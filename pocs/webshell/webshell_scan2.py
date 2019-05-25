#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 15:15
# @Author  : Goop
# @Site    : 
# @File    : webshell_scan2.py
# @Software: PyCharm

import re
import os.path
import time
import requests
import random
import base64
import html
from lib.core.data import paths
from lib.scheduler.loader import loadfakeuseragent
from plugin.extracts import getCharset

Timeout = 35

spider_ua_list = ['Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
                  'Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
                  'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
                  'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider'
                  ]

pwd = []
shell_pass_file = os.path.join(paths.DATA_PATH, 'Webshell_pass', 'shell_pass.txt')
with open(shell_pass_file, 'r')as p:
    pwd_list = p.readlines()
    dic = len(pwd_list) / 1000
    for pw in pwd_list:
        pw = pw.strip()
        pwd.append(pw)
sensitive_word_file = os.path.join(paths.DATA_PATH, 'Sensitivewords', 'filters.txt')
sen = []
with open(sensitive_word_file, 'r', encoding='UTF-8')as s:
    sensitive_word_list = s.readlines()
    for sensitive_word in sensitive_word_list:
        sensitive_word = sensitive_word.strip()
        sen.append(sensitive_word)


def random_ua():
    headers = {
        'User-Agent': loadfakeuseragent()
    }
    return headers


def random_spider_ua():
    spider_ua = {
        'User-Agent': random.choice(spider_ua_list)
    }
    return spider_ua


def check_webshell(url):
    webshell_list = []
    post_data = {}
    if '.asp' in url.lower():
        post_test = {'test_pass_test': 'response.write("test!!!")'}
        res = requests.post(url, data=post_test, timeout=Timeout, headers=random_ua())
        wrong_res = res.text
        post_test.clear()
        for i in range(0, int(dic) + 1):
            for text in pwd[i * 1000:(i + 1) * 1000]:
                post_data[text] = 'response.write("<|-password is %s-|>")' % text
            response = requests.post(url, data=post_data, headers=random_ua(), timeout=Timeout, )
            post_data.clear()
            time.sleep(1)
            if len(response.text) != len(wrong_res):
                if '"<|-password' not in response.text:
                    if '<|-password' in response.text:
                        pattern = re.search(r'[<][|][-](.*?)[-][|][>]', response.text)
                        find = "目标存在 Webshell 目标url: %s   %s" % (url, str(pattern.group(1)))
                        # return find
                        webshell_list.append(find)
    if '.aspx' in url.lower():
        post_test = {'test_pass_test': 'Response.Write("test!!!");'}
        res = requests.post(url, data=post_test, timeout=Timeout, headers=random_ua())
        wrong_res = res.text
        post_test.clear()
        for i in range(0, int(dic) + 1):
            for text in pwd[i * 1000:(i + 1) * 1000]:
                post_data[text] = 'Response.Write("<|-password is %s-|>");' % text
            response = requests.post(url, data=post_data, headers=random_ua(), timeout=Timeout)
            post_data.clear()
            time.sleep(1)
            if len(response.text) != len(wrong_res):
                if '"<|-password' not in response.text:
                    if '<|-password' in response.text:
                        pattern = re.search(r'[<][|][-](.*?)[-][|][>]', response.text)
                        find = "目标存在 Webshell 目标url: %s   %s" % (url, str(pattern.group(1)))
                        # return find
                        webshell_list.append(find)
    if '.jsp' in url.lower():
        post_test = {'test_pass_test': 'System.out.println("test!!!");'}
        res = requests.post(url, data=post_test, headers=random_ua(), timeout=Timeout)
        wrong_res = res.text
        post_test.clear()
        for i in range(0, int(dic) + 1):
            for text in pwd[i * 1000:(i + 1) * 1000]:
                post_data[text] = 'System.out.println("<|-password is %s-|>");' % text
            response = requests.post(url, data=post_data, headers=random_ua(), timeout=Timeout)
            post_data.clear()
            time.sleep(1)
            if len(response.text) != len(wrong_res):
                if '<|-password' in response.text:
                    pattern = re.search(r'[<][|][-](.*?)[-][|][>]', response.text)
                    find = "目标存在 Webshell 目标url: %s   %s" % (url, str(pattern.group(1)))
                    # return find
                    webshell_list.append(find)

    if '.php' in url.lower():
        post_test = {
            'test_pass_test': "@eval(base64_decode('ZWNobygicGFzc3dvcmQgaXMgdGVzdF9wYXNzX3Rlc3QiKTs='));"
        }
        res = requests.post(url, data=post_test, headers=random_ua(), timeout=Timeout)
        wrong_res = res.text
        post_test.clear()
        for i in range(0, int(dic) + 1):
            for text in pwd[i * 1000:(i + 1) * 1000]:
                aa = "<|-password is %s-|>" % text
                aaa = "echo('" + aa + "');"
                aaaa = base64.b64encode(aaa.encode('utf-8'))
                poc = "@eval(base64_decode('" + str(aaaa, 'utf-8') + "'));"
                post_data[text] = poc
            response = requests.post(url, data=post_data, headers=random_ua(), timeout=Timeout)
            post_data.clear()
            time.sleep(1)
            if len(response.text) != len(wrong_res):
                if '<|-password' in response.text:
                    pattern = re.search(r'[<][|][-](.*?)[-][|][>]', response.text)
                    find = "目标存在 Webshell 目标url: %s   %s" % (url, str(pattern.group(1)))
                    # return find
                    webshell_list.append(find)
    return webshell_list


def check_xebshell(url, sub, title):
    xebshell_list = []
    xebshell_check = ["name='pass'", 'name="pass"', 'name="envlpass"', "name='envlpass'", 'name="getpwd"',
                      "name='getpwd'"]
    submit_check = ["type='submit'", 'type="submit"']
    if title:
        for xebshell in xebshell_check:
            if xebshell in str(sub):
                find = "目标存在 Xebshell 目标url: %s   Title:%s" % (url, title)
                # return find
                xebshell_list.append(find)
        for submit in submit_check:
            if submit in str(sub):
                find = "目标存在提交按钮自行判断是否为大马 url: %s   Title:%s" % (url, title)
                # return find
                xebshell_list.append(find)
    return xebshell_list


def check_other(url, charset, title_encode_list):
    title_decode_list = list()
    # print('wwwwwwwwwwwwwwww')
    for title in title_encode_list:
        if b'&#' in title:
            try:
                title_bocai = html.unescape(title.decode(charset))
            except:
                try:
                    title_bocai = html.unescape(title.decode('utf-8'))
                except:
                    try:
                        title_bocai = html.unescape(title.decode('gbk'))
                    except:
                        title_bocai = ''

            title_decode_list.append(title_bocai.strip())
            result = []
            if title_decode_list:
                # for bc in sen:
                for title_b in title_decode_list:
                    # if bc in str(title_b):
                    find = "目标标题存在可疑html编码,查看标题自行判断 url: %s   Title:%s" % (url, title_b)
                    result.append(find)
                return result


def meta_redirect_title(url, meta_redirect_url, charset):
    redirect_req = requests.get(meta_redirect_url, timeout=6, headers=random_spider_ua())
    title_start = re.findall(b'<title>([\s\S]*?)</title>', redirect_req.content, re.I)
    return check_other(url, charset, title_start)


def js_redirect_title(url, js_redirect_url, charset):
    js_req = requests.get(js_redirect_url, timeout=6, headers=random_spider_ua())
    title_start = re.findall(b'<title>([\s\S]*?)</title>', js_req.content, re.I)
    return check_other(url, charset, title_start)


def poc(url, **kwargs):
    result_list = list()
    try:
        req = requests.get(url, headers=random_spider_ua(), timeout=Timeout)
        sub = re.findall(r'(<input.*?>)', req.text, re.I)
        title_first = re.findall(b'<title.*?>([\s\S]*?)</title>', req.content, re.I)
        meta_redirect = re.search(
            '''<meta .*(http-equiv=['"]?refresh['"]?.*)?content=['"].*url=([a-zA-z]+://[^\s]*)['"]+''', req.text, re.I)
        js_redirect = re.findall(r'''.*?location.href.*=.*['"]+(.*)['"]+''', req.text, re.I)
        charset = getCharset(req.text)
        if charset:
            charset = charset
        else:
            charset = 'utf-8'
        if title_first:
            title_encode_list = title_first
            title_start = title_first[0].strip()
            try:
                title_xebshell = title_start.decode(charset)
            except:
                try:
                    title_xebshell = title_start.decode()
                except:
                    try:
                        title_xebshell = title_start.decode('gbk')
                    except:
                        title_xebshell = ''
        else:
            title_encode_list = [b'Empty']
            title_start = b'Empty'
            title_xebshell = 'Empty'
        # print(title_encode_list, '\n')
        # print(title_xebshell, '\n')
        if req.status_code == 200 or req.status_code == 500:
            webshell = check_webshell(url)
            if webshell:
                for we in webshell:
                    result_list.append(we)
            if sub:
                xebsehll = check_xebshell(url, sub, title_xebshell)
                if xebsehll:
                    for xe in xebsehll:
                        result_list.append(xe)
            other = check_other(url, charset, title_encode_list)
            if other:
                for ot in other:
                    result_list.append(ot)
            if meta_redirect:
                if 'url=' in meta_redirect.group():
                    meta = meta_redirect_title(url, meta_redirect.group(2), charset)
                    if meta:
                        for me in meta:
                            result_list.append(me)
            if js_redirect:
                if 'http' in js_redirect[0]:
                    js = js_redirect_title(url, js_redirect[0], charset)
                    if js:
                        for j in js:
                            result_list.append(j)
                else:
                    js = js_redirect_title(url, url + '/' + js_redirect[0], charset)
                    if js:
                        for j in js:
                            result_list.append(j)
        return result_list
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.ChunkedEncodingError:
        pass
    except:
        pass


if __name__ == "__main__":
    a = poc('http://127.0.0.1/data.asp')
    print(a)

# <title>&#28023;&#21335;&#32593;&#25237;&#20449;&#35465;&#24179;&#21488;&#95;&#19971;&#26143;&#24425;&#31169;&#24425;&#25237;&#27880;&#20250;&#21592;&#32593;&#95;&#24320;&#22870;&#32467;&#26524;&#35270;&#39057;&#30452;&#25773;</title>
