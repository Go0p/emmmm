#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 14:08
# @Author  : Goop
# @Site    : 
# @File    : pass.py
# @Software: PyCharm

with open('WEBSHELL.txt', 'r', encoding="utf-8")as f:
    lines = f.readlines()
pw = []
for line in lines:
    pw.append(line.strip())
pw = sorted(list(set(pw)))
print(len(pw))
for p in pw:
    with open("2.txt", 'a', encoding='utf-8')as t:
        t.write(p + '\n')
