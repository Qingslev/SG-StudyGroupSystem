#!/user/bin/env python
#!-*-coding:utf-8 -*-
import sqlite3
import re
import logging

if __name__ =='__main__':
    conn = sqlite3.connect('sg2019.db')
    cursor = conn.cursor()
    try:
        cursor.execute('CREATE TABLE T_Member(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,sign_days INTEGER)')
    except:
        cursor.execute('DROP TABLE T_Member')
        cursor.execute('CREATE TABLE T_Member(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,sign_days INTEGER)')
    pathi = 'init.txt'
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
            m=re.match('[\u4e00-\u9fa5a-zA-Z0-9]+',x)
            name=m.group(0)
            cursor.execute('INSERT INTO T_Member VALUES(NULL,"'+name+'",0)')
            cursor.execute('CREATE TABLE T_'+name+' (id INTEGER PRIMARY KEY AUTOINCREMENT,date CHAR(6),tomato CHAR(2),sign CHAR(1))')
        else:
            pass
        count+=1

    while name != 'N':
        name=input('Any Other Member?(name/N）')
        if name =='N':
            pass
        else:
            m=re.match('[\u4e00-\u9fa5a-zA-Z0-9]+',name)
            name=m.group(0)
            cursor.execute('INSERT INTO T_Member VALUES(NULL,"'+name+'",0)')
            cursor.execute('CREATE TABLE T_'+name+' (id INTEGER PRIMARY KEY AUTOINCREMENT,date CHAR(6),tomato CHAR(2),sign CHAR(1))')

    cursor.execute('SELECT * FROM T_Member')
    s=cursor.fetchall()
    print(s)

    cursor.close()
    conn.commit()
    conn.close()
