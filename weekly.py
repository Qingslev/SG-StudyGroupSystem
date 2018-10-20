#!/user/bin/env python
#!-*-coding:utf-8 -*-

"""
　各个表的结构
T_date
id name potato presence
T_Member
id name
T_Name
id date potato presence
一些常见变量名的含义
member_list　正在组里的成员组成的表
date 前一天，即要处理的数据对应的日期
daily_tuples 当天的报表
"""
import sqlite3
from datetime import datetime, timedelta
import logging
import xlwt
logging.basicConfig(level=logging.INFO)

def getMemberList():
    cursor.execute('SELECT name FROM T_Member')
    member_tuples = cursor.fetchall()  # 这是个包含tuple的list
    member_list=[]
    for x in member_tuples:
        member_list.append(x[0])
    return member_list

def getWeeklyList():
    weekly_list = []
    now = datetime.now()
    for i in list(reversed(range(7))):
        date = (now - timedelta(days=(i + 1))).strftime('%y%m%d')
        weekly_list.append(date)
    logging.info(weekly_list)
    return weekly_list

def sortMemberList(member_list,weekly_list):
    member_tuples_sorted=[]
    for x in member_list:
        sum=0
        for date in weekly_list:
            cursor.execute('SELECT potato FROM T_'+x+' WHERE date="'+date+'"')
            potato=cursor.fetchall()
            if potato==[]:
                pass
            else:
                sum+=int(potato[0][0])
        member_tuples_sorted.append((x,sum))
    return sorted(member_tuples_sorted, key=lambda member: member[1], reverse=True)

def writeWeeklyOutput(member_tuples,weekly_list):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('table',cell_overwrite_ok=True)

    # 设置单元格宽度
    ws.col(0).width = 256 * 8
    ws.col(1).width = 256 * 32
    ws.col(2).width = 256 * 8
    ws.col(3).width = 256 * 8
    ws.col(4).width = 256 * 8
    ws.col(5).width = 256 * 8
    ws.col(6).width = 256 * 8
    ws.col(7).width = 256 * 8
    ws.col(8).width = 256 * 8
    ws.col(9).width = 256 * 8
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
    style3 = xlwt.easyxf('pattern: pattern solid, fore_colour _red1')
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
    font.colour_index = 23
    style4.font = font
    style4.borders = borders
    # style5
    style5 = xlwt.easyxf('pattern: pattern solid, fore_colour _red1')
    style5.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 1
    font.bold = True
    style5.font = font
    style5.borders = borders
    # style6
    style6 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey1')
    style6.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = xlwt.Style.colour_map['light_green']
    font.bold = True
    style6.font = font
    style6.borders = borders
    # style7
    style7 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey2')
    style7.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    style7.font = font
    style7.borders = borders

    ws.write(0, 0, 'RANK', style1)
    ws.write(0, 1, 'NAME', style1)
    ws.write(0, 2, 'MON', style1)
    ws.write(0, 3, 'TUE', style1)
    ws.write(0, 4, 'WED', style1)
    ws.write(0, 5, 'THU', style1)
    ws.write(0, 6, 'FIR', style1)
    ws.write(0, 7, 'SAT', style1)
    ws.write(0, 8, 'SUN', style1)
    ws.write(0, 9, 'TOAL', style1)
    for n,x in enumerate(member_tuples):
        if n<3:
            ws.write(n+1,0,n+1,style2)
            ws.write(n+1,1,x[0],style3)
            for m, date in enumerate(weekly_list):
                cursor.execute('SELECT potato FROM T_' + x[0] + ' WHERE date="' + date + '"')
                potato = cursor.fetchall()
                if potato==[]:
                    ws.write(n + 1, m + 2, '', style4)
                elif int(potato[0][0])>=20:
                    ws.write(n+1,m+2,potato[0][0],style5)
                else:
                    ws.write(n + 1, m + 2, potato[0][0], style4)
            ws.write(n+1,m+3,x[1],style3)
        else:
            ws.write(n + 1, 0, n + 1, style1)
            ws.write(n + 1, 1, x[0], style6)
            for m, date in enumerate(weekly_list):
                cursor.execute('SELECT potato FROM T_' + x[0] + ' WHERE date="' + date + '"')
                potato = cursor.fetchall()
                if potato==[]:
                    ws.write(n + 1, m + 2, '', style7)
                elif int(potato[0][0]) >= 20:
                    ws.write(n + 1, m + 2, potato[0][0], style5)
                else:
                    ws.write(n + 1, m + 2, potato[0][0], style7)
            ws.write(n + 1, m + 3, x[1], style6)

    wb.save('weekly\\'+weekly_list[-1]+'.xls')

if __name__=='__main__':
    conn = sqlite3.connect('sg.db')
    cursor = conn.cursor()
    date=datetime.now()
    assert date.weekday()==0,'Wrong Day!'

    member_list=getMemberList()
    weekly_list=getWeeklyList()
    member_tuples_sorted=sortMemberList(member_list,weekly_list)
    print(member_tuples_sorted)
    writeWeeklyOutput(member_tuples_sorted,weekly_list)
    cursor.close()
    conn.commit()
    conn.close()
