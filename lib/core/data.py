#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/30 12:24
# @Author  : Goop
# @Site    : 
# @File    : data.py
# @Software: PyCharm


from lib.core.datatype import AttribDict

# 路径
paths = AttribDict()
# 杂项
conf = AttribDict()

# 命令行参数
cmdLineOptions = AttribDict()
# 线程对象存储线程数
th = AttribDict()
# Hook requests
HCONF = conf