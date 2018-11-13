#!/user/bin/env python
#!-*-coding:utf-8 -*-

from datetime import datetime, timedelta
import re
import sqlite3
import logging
import xlwt
import os

logging.basicConfig(level=logging.INFO)
"""
　各个表的结构
T_date
id name tomato sign
T_Member
id name sign_days
T_Name
id date tomato sign
一些常见变量名的含义
member_list　正在组里的成员组成的表
date 前一天，即要处理的数据对应的日期
daily_tuples 当天的报表
"""

def getDate():
    now=datetime.now()
    date=(now-timedelta(days=1)).strftime('%y%m%d')
    return date

def readDailyInput(date):
    pathi='/volumes/macs/projects/SG/data/'+date+'.txt'
    # pathi = '/volumes/macs/projects/SG/test.txt'
    fi=open(pathi,'r',encoding='utf-8')
    s=fi.read()
    fi.close()
    list=s.split('\n')
    name=''
    tomato=''
    count=1
    daily_tuples=[]
    for x in list:
        if count%3==1:
            # name=re.sub('[\s+\.\!\-\/_,$%^*(+\"\')]+|[+——()?【】“” :：！，。？、~@#￥%……&*（）]+', '', x)
            m=re.match('[\u4e00-\u9fa5a-zA-Z0-9]+',x)
            name=m.group(0)
        elif count%3==2:
            if re.match(r'.*[请].*[假].*',x):
                daily_tuples.append((name,0,'1'))
            else:
                tomato=re.findall(r'\d+',x)
                if int(tomato[0])<2:
                    daily_tuples.append((name,tomato[0],'0'))
                else:
                    daily_tuples.append((name,tomato[0],'1'))
        count+=1
    return sorted(daily_tuples, key=lambda member: int(member[1]),reverse=True)

def getMemberList():
    cursor.execute('SELECT name FROM T_Member')
    member_tuples = cursor.fetchall()  # 这是个包含tuple的list
    member_list=[]
    for x in member_tuples:
        member_list.append(x[0])
    return member_list

def initNameTable(daily_tuples,member_list):
    member_list_today = []
    for x in daily_tuples:
        member_list_today.append(x[0])
    for x in member_list_today:
        if x in member_list:
            pass
        else:
            input('New member:'+x)
            try:
                cursor.execute('CREATE TABLE T_'+x+' (id INTEGER PRIMARY KEY AUTOINCREMENT,date CHAR(6),tomato CHAR(2),sign CHAR(1))')
            except:
                cursor.execute('DROP TABLE T_'+x)
                cursor.execute('CREATE TABLE T_'+x+' (id INTEGER PRIMARY KEY AUTOINCREMENT,date CHAR(6),tomato CHAR(2),sign CHAR(1))')
            cursor.execute('INSERT INTO T_Member VALUES(NULL,"'+x+'",0)')

def writeDailyTable(daily_tuples,date,member_list):
    try:
        cursor.execute('CREATE TABLE T_' + date + ' (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,tomato CHAR(2),sign CHAR(1))')  # 0 False 1 True
    except:
        cursor.execute('DROP TABLE T_'+date)
        try:
            for x in member_list:
        	    cursor.execute('DELETE FROM T_'+x+' WHERE date="'+date+'"')
        except:
        	pass
        cursor.execute('CREATE TABLE T_' + date + ' (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,tomato CHAR(2),sign CHAR(1))')  # 0 False 1 True
        cursor.execute('SELECT sign_days FROM T_Member WHERE name="'+xn[0]+'"')
        lines=cursor.fetchall()
        sign_days=lines[0][0]+1
        cursor.execute('UPDATE T_Member SET sign_days='+str(sign_days)+' WHERE name="'+xn[0]+'"')

    for x in daily_tuples:
        cursor.execute("INSERT INTO T_"+date+" VALUES (NULL,'"+x[0]+"','"+str(x[1])+"','"+x[2]+"')")

    member_list_today=[]
    for x in daily_tuples:
        member_list_today.append(x[0])

    for x in member_list:
        if x in member_list_today:
            pass
        else:
            cursor.execute("INSERT INTO T_"+date+" VALUES(NULL,'"+x+"','0','0')")

def writeNameTable(date,member_list):
    cursor.execute('SELECT name,tomato,sign FROM T_'+date)
    daily_list=cursor.fetchall()
    sign_days=0
    for xn in daily_list:#([name tomato sign],[]...)
        if xn[2]=='1':
        	cursor.execute('SELECT sign_days FROM T_Member WHERE name="'+xn[0]+'"')
        	lines=cursor.fetchall()
        	sign_days=lines[0][0]+1
        	cursor.execute('UPDATE T_Member SET sign_days='+str(sign_days)+' WHERE name="'+xn[0]+'"')
        else:
        	cursor.execute('UPDATE T_Member SET sign_days=0 WHERE name="'+xn[0]+'"')
        cursor.execute('INSERT INTO T_'+xn[0]+' VALUES (NULL,"'+date+'","'+xn[1]+'","'+xn[2]+'")')#date tomato sign

def getQuitMember(member_list):
    quit_member_list=[]
    weekday_list=[]
    now = datetime.now()
    weekday = now.weekday()
    for i in range(weekday + 1):
        date = (now - timedelta(days=i)).strftime('%y%m%d')
        weekday_list.append(date)
    for x in member_list:
        sign_list = []
        for y in weekday_list:
            cursor.execute('SELECT sign FROM T_'+x+' WHERE date="'+y+'"')
            sign=cursor.fetchall()
            if ('0',) in sign:
                sign_list.append(y)
        if len(sign_list)>=2:
            input('Quit:'+x)
            quit_member_list.append((x,sign_list[0],sign_list[1]))
    return quit_member_list

def writeDailyOutput1(date,quit_member_list):
    cursor.execute('SELECT name,tomato,sign FROM T_' + date)
    daily_list = cursor.fetchall()

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(date,cell_overwrite_ok=True)

    # 设置单元格宽度
    ws.col(0).width = 256 * 8
    ws.col(1).width = 256 * 32
    ws.col(2).width = 256 * 8
    # 设置对其格式
    alignment = xlwt.Alignment()  # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_LEFT  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    # 设置填充色
    xlwt.add_palette_colour('_red1', 0x21)
    wb.set_colour_RGB(0x21, 214, 88, 66)  # 每次要用不同的x+num 8-63之间
    xlwt.add_palette_colour('_red2', 0x22)
    wb.set_colour_RGB(0x22, 226, 135, 120)
    xlwt.add_palette_colour('_grey1', 0x23)
    wb.set_colour_RGB(0x23, 188, 188, 188)
    xlwt.add_palette_colour('_grey2', 0x24)
    wb.set_colour_RGB(0x24, 234, 234, 234)
    # 设置边框
    borders = xlwt.Borders()  # Create Borders
    borders.left = xlwt.Borders.THIN
    # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = xlwt.Style.colour_map['white']
    borders.right_colour = xlwt.Style.colour_map['white']
    borders.top_colour = xlwt.Style.colour_map['white']
    borders.bottom_colour = xlwt.Style.colour_map['white']
    # style1
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey1')
    style1.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 1
    style1.font = font
    style1.borders = borders
    # style2
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour _red1')
    style2.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 1
    style2.font = font
    style2.borders = borders
    # style3
    style3 = xlwt.easyxf('pattern: pattern solid, fore_colour _red2')
    style3.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = xlwt.Style.colour_map['light_green']
    font.bold = True
    style3.font = font
    style3.borders = borders
    # style4
    style4 = xlwt.easyxf('pattern: pattern solid, fore_colour _red2')
    style4.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = xlwt.Style.colour_map['light_green']
    style4.font = font
    style4.borders = borders
    # style5
    style5 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey1')
    style5.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    font.bold = True
    style5.font = font
    style5.borders = borders
    # style6
    style6 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey2')
    style6.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    style6.font = font
    style6.borders = borders

    ws.write(0, 0, 'RANK', style1)
    ws.write(0, 1, 'NAME', style1)
    ws.write(0, 2, 'TODO', style1)

    for i, x in enumerate(daily_list):
        if i < 3:
            ws.write(i + 1, 0, i+1, style2)
            ws.write(i + 1, 1, x[0], style3)
            ws.write(i + 1, 2, x[1], style4)
        else:
            if x[1]=='0':
                if x[2]=='0':
                    ws.write(i + 1, 0, i + 1, style1)
                    ws.write(i + 1, 1, x[0], style5)
                    ws.write(i + 1, 2, '缺勤', style6)
                else:
                    ws.write(i + 1, 0, i + 1, style1)
                    ws.write(i + 1, 1, x[0], style5)
                    ws.write(i + 1, 2, '请假', style6)
            else:
                ws.write(i + 1, 0, i+1, style1)
                ws.write(i + 1, 1, x[0], style5)
                ws.write(i + 1, 2, x[1], style6)
    n=0
    for x in quit_member_list:
        ws.write(i+2+n+0,0,'Quit',style1)
        ws.write(i+2+n+0,1,x[0],style5)
        ws.write(i+2+n+0,2,'',style6)
        ws.write(i+2+n+1,0,'',style1)
        ws.write(i+2+n+1,1,x[1],style5)
        ws.write(i+2+n+1,2,'',style6)
        ws.write(i+2+n+2,0,'',style1)
        ws.write(i+2+n+2,1,x[2],style5)
        ws.write(i+2+n+2,2,'',style6)
        n+=3
    wb.save('/volumes/macs/projects/SG/daily/'+date+'_1.xls')#?

def writeDailyOutput2(date):
    cursor.execute('SELECT name,sign_days FROM T_Member')
    daily_list = cursor.fetchall()

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(date,cell_overwrite_ok=True)

    # 设置单元格宽度
    ws.col(0).width = 256 * 8
    ws.col(1).width = 256 * 32
    ws.col(2).width = 256 * 8
    # 设置对其格式
    alignment = xlwt.Alignment()  # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_LEFT  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    # 设置填充色
    xlwt.add_palette_colour('_blue1', 0x21)
    wb.set_colour_RGB(0x21, 10, 10, 128)  # 每次要用不同的x+num 8-63之间
    xlwt.add_palette_colour('_blue2', 0x22)
    wb.set_colour_RGB(0x22, 70, 130, 180)
    xlwt.add_palette_colour('_grey1', 0x23)
    wb.set_colour_RGB(0x23, 188, 188, 188)
    xlwt.add_palette_colour('_grey2', 0x24)
    wb.set_colour_RGB(0x24, 234, 234, 234)
    # 设置边框
    borders = xlwt.Borders()  # Create Borders
    borders.left = xlwt.Borders.THIN
    # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = xlwt.Style.colour_map['white']
    borders.right_colour = xlwt.Style.colour_map['white']
    borders.top_colour = xlwt.Style.colour_map['white']
    borders.bottom_colour = xlwt.Style.colour_map['white']
    # style1
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey1')
    style1.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 1
    style1.font = font
    style1.borders = borders
    # style2
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour _blue1')
    style2.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 1
    style2.font = font
    style2.borders = borders
    # style3
    style3 = xlwt.easyxf('pattern: pattern solid, fore_colour _blue2')
    style3.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = xlwt.Style.colour_map['light_green']
    font.bold = True
    style3.font = font
    style3.borders = borders
    # style4
    style4 = xlwt.easyxf('pattern: pattern solid, fore_colour _blue2')
    style4.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = xlwt.Style.colour_map['light_green']
    style4.font = font
    style4.borders = borders
    # style5
    style5 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey1')
    style5.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    font.bold = True
    style5.font = font
    style5.borders = borders
    # style6
    style6 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey2')
    style6.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    style6.font = font
    style6.borders = borders

    ws.write(0, 0, 'RANK', style1)
    ws.write(0, 1, 'NAME', style1)
    ws.write(0, 2, 'DAYS', style1)
    daily_list=sorted(daily_list, key=lambda member: int(member[1]),reverse=True)
    for i, x in enumerate(daily_list):
        if i < 3:
            ws.write(i + 1, 0, i+1, style2)
            ws.write(i + 1, 1, x[0], style3)
            ws.write(i + 1, 2, x[1], style4)
        else:
            ws.write(i + 1, 0, i+1, style1)
            ws.write(i + 1, 1, x[0], style5)
            ws.write(i + 1, 2, x[1], style6)
    wb.save('/volumes/macs/projects/SG/daily/'+date+'_2.xls')

if __name__ =='__main__':
    conn = sqlite3.connect('sg.db')
    cursor = conn.cursor()

    date=getDate()
    input('Good Morning!')

    l=readDailyInput(date)

    m=getMemberList()
    initNameTable(l,m)
    conn.commit()
    m=getMemberList()

    writeDailyTable(l,date,m)
    conn.commit()

    writeNameTable(date,m)
    conn.commit()

    quit_member_list=getQuitMember(m)

    writeDailyOutput1(date,quit_member_list)
    writeDailyOutput2(date)
    print('OK!')

    for x in quit_member_list:
        cursor.execute('DELETE FROM T_Member WHERE name="' + x[0] + '"')

    cursor.close()
    conn.commit()
    conn.close()
