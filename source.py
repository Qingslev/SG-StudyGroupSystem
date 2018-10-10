#!/user/bin/env python
#!-*-coding:utf-8 -*-

from datetime import datetime, timedelta

#录入时间
now=datetime.now()
day=(now-timedelta(days=1)).strftime('%y%m%d')

#录入文件
pathi='/projects/SG/data_unsort/'+day+'.txt'
fi=open(pathi,'r',encoding='utf-8')
s=fi.read()[1:]#有个不知道什么字符
fi.close()

#处理文件
data_list=s.split()
name=''
potato=0
count=1
member_tuples=[]
for x in data_list:
    if count%3==1:
        name=x
    elif count%3==2:
        pass
    elif count%3==0:
        potato=int(x)
        member_tuples.append((name, potato))
    count=count+1
member_tuples=sorted(member_tuples, key=lambda member: member[1],reverse=True)

#写入文件
patho='/projects/SG/data_sorted/'+day+'.txt'
fo=open(patho, 'w',encoding='utf-8')
fo.write(day+'\n')
for x in member_tuples:
    fo.write(x[0]+'  '+str(x[1])+'\n')
fo.close()

