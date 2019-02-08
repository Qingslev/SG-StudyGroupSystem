import sqlite3

conn = sqlite3.connect('sg2019.db')
cursor = conn.cursor()
def changedata(name,date,tomato):
    cursor.execute('UPDATE T_'+name+' SET tomato='+tomato+' WHERE date = '+date)
    cursor.execute('UPDATE T_'+name+' SET sign=1 WHERE date = '+date)
    cursor.execute('SELECT * FROM T_'+name)
    name_tuples=cursor.fetchall()
    print(name_tuples)
    sign_days=0
    for x in name_tuples:
        if x[3]=='1':
            sign_days+=1
        else:
            sign_days=0
    cursor.execute('UPDATE T_Member SET sign_days='+str(sign_days))
    cursor.execute('SELECT * FROM T_Member')
    s=cursor.fetchall()
    print(s)

def changename(name_1,name_2):
    cursor.execute('SELECT * FROM T_'+name_1)
    name_1_tuples=cursor.fetchall()
    cursor.execute('CREATE TABLE T_'+name_2+' (id INTEGER PRIMARY KEY AUTOINCREMENT,date CHAR(6),tomato CHAR(2),sign CHAR(1))')
    cursor.execute('INSERT INTO T_Member VALUES(NULL,"'+name_2+'",0)')
    cursor.execute('DELETE FROM T_Member WHERE name="' + name_1 + '"')
    cursor.execute
    for x in name_1_tuples:
        cursor.execute('INSERT INTO T_'+name_2+' VALUES (NULL,"'+x[1]+'","'+x[2]+'","'+xn[3]+'")')
    cursor.execute('SELECT * FROM T_'+name_2)
    s=cursor.fetchall()
    print(s)


# changedata('萌','190101','3')
cursor.close()
conn.commit()
conn.close()
