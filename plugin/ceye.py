#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 15:54
# @Author  : Goop
# @Site    : 
# @File    : ceye.py
# @Software: PyCharm

import requests
import random
from string import ascii_lowercase
from lib.api.config.config import ConfigFileParser

token = ConfigFileParser().CEyeToken()
type = ['dns', 'http']
filter = ''.join([random.choice(ascii_lowercase) for _ in range(10)])
print(filter)
a = 'http://api.ceye.io/v1/records?token={token}&type={type}&filter={filter}'.format(token=token, type=type[1],
                                                                                     filter='name')
print(a)
req = requests.get(a, timeout=15)
print(req.text)


def getDnsRecord():
    pass


def getHttpRecord():
    pass
