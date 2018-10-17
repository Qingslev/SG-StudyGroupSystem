#!/user/bin/env python
#!-*-coding:utf-8 -*-
import sqlite3
import re
import logging

if __name__ =='__main__':
    conn = sqlite3.connect('sg.db')
    cursor = conn.cursor()
    answer=input('Replace T_Member?(Y/N)')
    assert answer=='Y' or answer=='N','wrong input'
    if answer=='N':
        pass
    if answer=='Y':
        cursor.execute('DROP TABLE T_Member')
        cursor.execute('CREATE TABLE T_Member (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT)')
        while answer=='Y':
            name=input('Name?')
            name_filtered = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”:：！，。？、~@#￥%……&*（）]+', '', name)
            logging.info('name=%s', name_filtered)
            cursor.execute('CREATE TABLE T_' + name_filtered + ' (id INTEGER PRIMARY KEY AUTOINCREMENT,date CHAR(6),potato CHAR(2),presence CHAR(1))')
            cursor.execute('INSERT INTO T_Member VALUES(NULL,"'+name_filtered+'")')
            answer=input('Any other members?(Y/N)')
    cursor.close()
    conn.commit()
    conn.close()
