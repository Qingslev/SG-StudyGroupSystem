#!/user/bin/env python
#!-*-coding:utf-8 -*-

from datetime import datetime, timedelta
import re
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
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
daily_list 当天的报表
"""

def getDate():
    now=datetime.now()
    date=(now-timedelta(days=1)).strftime('%y%m%d')
    return date

def initNameTable():
    name=input('Name?')
    name=re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”:：！，。？、~@#￥%……&*（）]+', '',name)
    logging.info('name=%s',name)
    cursor.execute('CREATE TABLE T_'+name+' (id INTEGER PRIMARY KEY AUTOINCREMENT,date CHAR(6),potato CHAR(2),presence CHAR(1))')
    cursor.execute('INSERT INTO T_Member VALUES(NULL,"'+name+'")')

def readDailyInput(date):
    pathi='/projects/SG/data/'+date+'.md'
    fi=open(pathi,'r',encoding='utf-8')
    s=fi.read()#有个不知道什么字符
    fi.close()
    list=s.split()
    name=''
    potato=0
    count=1
    daily_tuples=[]
    for x in list:
        if count%2==1:
            name=x[0:-1]
            name=re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”:：！，。？、~@#￥%……&*（）]+', '', name)
        elif count%2==0:
            potato=int(x)
            daily_tuples.append((name, potato))
        count=count+1
    return sorted(daily_tuples, key=lambda member: member[1],reverse=True)

def writeDailyTable(daily_tuples,date):
    # cursor.execute('DROP TABLE T_'+date)
    cursor.execute('CREATE TABLE T_'+date+' (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,potato CHAR(2),presence CHAR(1))')#0 False 1 True
    for x in daily_tuples:
        if x[1]>=2:
            cursor.execute("INSERT INTO T_"+date+" VALUES (NULL,'"+x[0]+"','"+str(x[1])+"','1')")#表内的数据全部都是字符串，所以不能用SQLine内置的数学方法
        else:
            cursor.execute("INSERT INTO T_"+date+" VALUES (NULL,'"+x[0]+"','"+str(x[1])+"','0')")

    member_list_today=[]
    for x in daily_tuples:
        member_list_today.append(x[0])
    cursor.execute('SELECT name FROM T_Member')
    member_list=cursor.fetchall() #这是个包含tuple的list
    for x in member_list:
        if x[0] in member_list_today:
            pass
        else:
            reason=input('Does '+x[0]+' has asked for leave or is absent?(L/A)')
            assert reason=='L'or reason=='A','wrong input!'
            if reason=='L':
                cursor.execute("INSERT INTO T_"+date+" VALUES(NULL,'"+x[0]+"','0','1')")
            elif reason=='A':
                cursor.execute("INSERT INTO T_"+date+" VALUES(NULL,'"+x[0]+"','0','0')")

def writeNameTable(date):
    cursor.execute('SELECT name FROM T_Member')
    member_list=cursor.fetchall()
    cursor.execute('SELECT name,potato,presence FROM T_'+date)
    daily_list=cursor.fetchall()
    for x in member_list:
        for xn in daily_list:#([name potato presence],[]...)
            if x[0]==xn[0]:
                cursor.execute('INSERT INTO T_'+xn[0]+' VALUES (NULL,"'+date+'","'+xn[1]+'","'+xn[2]+'")')#date potato presence

def getQuitMember():
    cursor.execute('SELECT name FROM T_Member')
    member_list=cursor.fetchall()
    quit_member=[]
    for x in member_list:
        cursor.execute('SELECT presence FROM T_'+x[0])
        presence_list=cursor.fetchall()
        absence=0
        for i in presence_list:
            if i[0]=='0':
                absence+=1
        if absence>=2:
            print('%s should quit.',x[0])
            quit_member.append(x[0])
    return quit_member

def writeDailyOutput(date,quit_member):
    patho = '/projects/SG/daily/' + date + '.txt'
    fo = open(patho, 'w', encoding='utf-8')
    cursor.execute('SELECT name,potato FROM T_' + date)
    daily_list = cursor.fetchall()
    fo.write(date+'\n\n')
    fo.write('Rank | Name | Potato\n')
    fo.write('-----|------|------\n')
    for i,x in enumerate(daily_list):
        fo.write(str(i+1)+' | '+x[0]+' | '+x[1]+'\n')
    for x in quit_member:
        fo.write('\nQuit Member:'+x)
    fo.close()

def dropNameTable(name):
    cursor.execute('DROP TABLE T_'+name)
    cursor.execute('DELETE FROM T_Member WHERE name="'+name+'"')

if __name__ =='__main__':
    conn = sqlite3.connect('sg.db')
    cursor = conn.cursor()
    date=getDate()

    print('Good Morning!')

    answer='Y'
    while answer=='Y':
        answer=input('Is there any new member?(Y/N)')
        assert answer=='Y' or answer=='N','wrong input!'
        if answer=='Y':
            initNameTable()



    s=readDailyInput(date)
    print('Successfully Input the Data!')
    print(s)

    writeDailyTable(s,date)

    writeNameTable(date)

    quit_member=getQuitMember()

    writeDailyOutput(date,quit_member)
    print('Successfully Output the Daily Table!')

    for x in quit_member:
        dropNameTable(x)
    print('Successfully Drop the Table of the quited members')

    cursor.close()
    conn.commit()
    conn.close()
