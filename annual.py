#!/user/bin/env python
#!-*-coding:utf-8 -*-

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

import sqlite3
from datetime import datetime, timedelta
import logging
import xlwt
logging.basicConfig(level=logging.INFO)

def writeAnnualOutput(id,name,name_tuples):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('table',cell_overwrite_ok=True)

    # 设置单元格宽度
    for i in range(0,8):
        ws.col(i).width = 256 * 10

    # 设置对其格式
    alignment = xlwt.Alignment()  # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    # 设置填充色
    xlwt.add_palette_colour('_yellow', 0x21)
    wb.set_colour_RGB(0x21, 255, 154, 48)  
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
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour _yellow')
    style1.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 960
    font.colour_index = 1
    style1.font = font
    style1.borders = borders
    # style2
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey1')
    style2.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 300
    font.colour_index = xlwt.Style.colour_map['light_green']
    style2.font = font
    style2.borders = borders
    # style3
    style3 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey1')
    style3.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 1
    style3.font = font
    style3.borders = borders
    # style4
    style4 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey2')
    style4.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    style4.font = font
    style4.borders = borders
    # style5
    style5 = xlwt.easyxf('pattern: pattern solid, fore_colour _yellow')
    style5.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 480
    font.colour_index = 1
    style5.font = font
    style5.borders = borders
    # style6
    style6 = xlwt.easyxf('pattern: pattern solid, fore_colour _grey2')
    style6.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    font.bold=True
    style6.font = font
    style6.borders = borders
    # style7
    style7 = xlwt.easyxf('pattern: pattern solid, fore_colour white')
    style7.alignment = alignment
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.height = 240
    font.colour_index = 23
    style7.font = font
    style7.borders = borders

    ws.write_merge(0,0,0,6,'2018',style1)
    ws.write_merge(1,2,0,1,name,style2)

    ws.write(1,2,'ID',style3)
    ws.write(2,2,id,style4)

    ws.write_merge(1,1,3,4,'签到总数',style3)
    sum_days=0
    for x in name_tuples:
        if x[3]=='1':
            sum_days+=1
    ws.write_merge(2,2,3,4,sum_days,style4)

    ws.write_merge(1,1,5,6,'累计番茄总数',style3)
    sum_tomatos=0
    for x in name_tuples:
        sum_tomatos=sum_tomatos+int(x[2])
    ws.write_merge(2,2,5,6,sum_tomatos,style4)

    row=3

    for x in name_tuples:
        if '1811' in x[1]:
            ws.write_merge(row,row,0,6,'NOVEMBER',style5)
            ws.write(row+1, 0, 'MON', style3)
            ws.write(row+1, 1, 'TUE', style3)
            ws.write(row+1, 2, 'WED', style3)
            ws.write(row+1, 3, 'THU', style3)
            ws.write(row+1, 4, 'FIR', style3)
            ws.write(row+1, 5, 'SAT', style3)
            ws.write(row+1, 6, 'SUN', style3)
            row+=2
            break
    for x in name_tuples:
        if '1812' in x[1]:
            row+=2
            break
        day = datetime.strptime(x[1],'%y%m%d')
        ws.write(row,day.weekday(),x[1][4:6],style6)
        ws.write(row+1,day.weekday(),x[2],style7)
        if day.weekday()==6:
            row+=2

    for x in name_tuples:
        if '1812' in x[1]:
            ws.write_merge(row,row,0,6,'DECEMBER',style5)
            ws.write(row+1, 0, 'MON', style3)
            ws.write(row+1, 1, 'TUE', style3)
            ws.write(row+1, 2, 'WED', style3)
            ws.write(row+1, 3, 'THU', style3)
            ws.write(row+1, 4, 'FIR', style3)
            ws.write(row+1, 5, 'SAT', style3)
            ws.write(row+1, 6, 'SUN', style3)
            row+=2
            break
    for x in name_tuples:
        if '1811' in x[1]:
            continue
        day = datetime.strptime(x[1],'%y%m%d')
        ws.write(row,day.weekday(),x[1][4:6],style6)
        ws.write(row+1,day.weekday(),x[2],style7)
        if day.weekday()==6:
            row+=2
        

    wb.save('2018//'+name+'.xls')

if __name__=='__main__':
    conn = sqlite3.connect('sg.db')
    cursor = conn.cursor()
    date=datetime.now()

    cursor.execute('SELECT * FROM T_Member')
    member_tuples = cursor.fetchall()  # 这是个包含tuple的list
    for x in member_tuples:
        cursor.execute('SELECT * FROM T_'+x[1])
        name_tuples=cursor.fetchall()
        writeAnnualOutput(x[0],x[1],name_tuples)

    cursor.close()
    conn.commit()
    conn.close()
