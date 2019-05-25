#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/30 11:31
# @Author  : Goop
# @Site    : 
# @File    : setting.py
# @Software: PyCharm

import os.path
import difflib
import requests
import random
import re
from urllib.parse import urlparse
from lib.core.conf import BANNER
from lib.core.data import paths
from thirdlib.colorama import Back, Fore, Style, init

init(autoreset=True)


class Outputscreen:
    """
    显示颜色类
    """

    def info(self, s):
        print(Style.BRIGHT + Fore.WHITE + '[+] ' + str(s) + Fore.RESET + Style.RESET_ALL)

    def success(self, s):
        print(Style.BRIGHT + Fore.GREEN + '[*] ' + str(s) + Fore.RESET + Style.RESET_ALL)

    def ensuccess(self, s):
        print(Style.BRIGHT + Fore.GREEN + str(s) + Fore.RESET + Style.RESET_ALL)

    def resuccess(self, s):
        print(Style.BRIGHT + Fore.GREEN + '\n\n[Report] ' + str(s) + Fore.RESET + Style.RESET_ALL)

    def warning(self, s):
        print(Style.BRIGHT + Fore.CYAN + '[!] ' + str(s) + Fore.RESET + Style.RESET_ALL)

    # for printProgress
    def Progress(self, s):
        print(Style.BRIGHT + Fore.CYAN + str(s) + Fore.RESET + Style.RESET_ALL, end="")

    def error(self, s):
        print(Style.BRIGHT + Fore.RED + '[-] ' + str(s) + Fore.RESET + Style.RESET_ALL)

    def nerror(self, s):
        print(Style.BRIGHT + Fore.RED + '\n\n[-] ' + str(s) + Fore.RESET + Style.RESET_ALL)

    # for banner
    def blue(self, s):
        print(Style.BRIGHT + Fore.BLUE + str(s) + Fore.RESET + Style.RESET_ALL)


outputscreen = Outputscreen()


def setPaths():
    """
    设置全局绝对路径
    :return:
    """
    root_path = paths.ROOT_PATH
    paths.DATA_PATH = os.path.join(root_path, "data")
    paths.OUTPUT_PATH = os.path.join(root_path, "output")
    paths.POCS_PATH = os.path.join(root_path, "pocs")
    paths.CONFIG_PATH = os.path.join(root_path, "toolkit.conf")
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)
    if not os.path.exists(paths.DATA_PATH):
        os.mkdir(paths.DATA_PATH)
    paths.WEAK_PASS = os.path.join(paths.DATA_PATH, "pass100.txt")
    paths.LARGE_WEAK_PASS = os.path.join(paths.DATA_PATH, "pass1000.txt")
    paths.UA_LIST_PATH = os.path.join(paths.DATA_PATH, "user-agents.txt")


def banner():
    """
    打印banner
    :return:
    """
    outputscreen.blue(BANNER)


def urlSimilarCheck(url):
    """
    url相似度分析，当url路径和参数键值类似时
    :param url:
    :return:
    """
    pass


def getTitle(input):
    """
    Get title from html-content/ip/url

    :param input:html-content OR ip OR url
    :return text in <title>
    :except return string:'NULL'
    """
    try:
        if '<title>' in input:
            content = input
        else:
            url = 'http://' + input if '://' not in input else input
            content = requests.get(url, timeout=3).content
        return re.findall(b'<title>([\s\S]*)</title>', content)[0].strip()
    except Exception:
        return ''


def url200or404Check(url):
    """
    url死链判断，筛选出页面内404的页面
    :return:degree of similarity < 0.85 return True
    """
    parse_result = urlparse(url)
    random_num = ''.join(str(i) for i in random.sample(range(0, 9), 5))
    url_404 = "%s://%s/this_is_404_page_%s" % (parse_result.scheme, parse_result.netloc, random_num)
    try:
        standard_text = requests.get(url_404).text
    except:
        pass
    try:
        text = requests.get(url).text
    except:
        pass
    degree_of_similarity = difflib.SequenceMatcher(None, standard_text, text).quick_ratio()
    if degree_of_similarity < 0.85:
        return True
    return False
