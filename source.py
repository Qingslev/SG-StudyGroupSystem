#!/user/bin/env python
#!-*-coding:utf-8 -*-
#!@Time     :2018/10/6 2018/10/6
#!@Author   :Qingslev
#!@File     :.py

#inistialize the class
# class Member(object):
#     def __init__(self,name,potato=2):
#         self.name=name
#         self.potato=potato
#     def __str__(self):
#         return 'Member: %s Potato:%s' %self.name %self.potato

#input data
print("Enter 'END' to quit...")
name=''
member_tuples=[]
while True:
    name=input('Member:')
    assert isinstance(name,str),'TypeError'
    if name=='END':
        break
    potato=int(input('Potato:'))
    assert potato>0,'ValueError'
    member_tuples.append((name,potato))
member_tuples=sorted(member_tuples, key=lambda member: member[1])
print(member_tuples)
