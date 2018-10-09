#!/user/bin/env python
#!-*-coding:utf-8 -*-
#!@Time     :2018/10/9
#!@Author   :Qingslev
#!@File     :.py

import time

#录入文件
date=time.strftime('%y%m%d',time.localtime(time.time()))
pathi='/projects/SG/data_unsort/'+str(int(date)-1)+'.md'
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
patho='/projects/SG/data_sorted/'+date+'.md'
fo=open(patho, 'w',encoding='utf-8')
for x in member_tuples:
    lines=x[0]+'  '+str(x[1])+'\n'
    fo.write(lines)
fo.close()
