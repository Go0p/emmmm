#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/30 12:33
# @Author  : Goop
# @Site    : 
# @File    : loader.py
# @Software: PyCharm

import importlib.util
import sys
import os
import time
import random
import queue
from lib.core.data import conf, paths, cmdLineOptions
from lib.core.setting import outputscreen
from lib.api.zoomeye.pack import ZoomEyeSearch
from lib.api.google.pack import GoogleSearch


# 加载pocs中的脚本文件
def loadPayload():
    conf.MODULE_PLUGIN = dict()
    # 遍历脚本,脚本名和路径对应 name->path
    for i in range(0, len(conf.MODULE_NAME)):
        name = conf.MODULE_NAME[i]
        path = conf.MODULE_FILE_PATH[i]
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            module_obj = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_obj)
            for each in ['poc']:
                if not hasattr(module_obj, each):
                    error_msg = "[Warning] Can't find essential method:'%s()' in current %s，Please modify your script/PoC." % (
                        each, name)
                    outputscreen.error(error_msg)
                else:
                    conf.MODULE_PLUGIN[name] = module_obj
        except:
            raise
            # error_msg = "Your current script [%s] caused this exception" % name
            # sys.exit(outputscreen.error(error_msg))


# 设置单/文件目标模块
def setModule():
    conf.queue = queue.Queue()
    if conf.TARGET_MODE == 'SINGLE':
        load_target_mode()
    elif conf.TARGET_MODE == 'FILE':
        load_file_mode()
    elif conf.TARGET_MODE == 'API':
        load_api_mode()
    if conf.PROXY_MODE == 'PROXY':
        load_proxy_ip()
    if conf.UA_MODE == "UA":
        load_ua()
    if conf.COOKIE_MODE == "COOKIE":
        load_cookie()
    outputscreen.info('Total: %s' % str(conf.queue.qsize()))


# 加载单个目标
def load_target_mode():
    for name, exp in conf.MODULE_PLUGIN.items():
        module = dict()
        if '://' not in str(conf.INPUT_TARGET_URL):
            conf.INPUT_TARGET_URL = 'http://' + str(conf.INPUT_TARGET_URL)
        # 目标
        module["sub"] = str(conf.INPUT_TARGET_URL)
        # importlib导入的脚本 <module 'xx.py' from 'path/xx.py'>
        module["poc"] = exp
        # 脚本文件名
        module["name"] = name
        conf.queue.put(module)


# 加载文件目标
def load_file_mode():
    subs = []
    try:
        with open(conf.INPUT_FILE_PATH)as p:
            lines = p.readlines()
        for line in lines:
            line = line.strip()
            subs.append(line)
        # 去重排序
        subs = sorted(list(set(subs)))
        for su in subs:
            for name, exp in conf.MODULE_PLUGIN.items():
                sub = su.strip()
                if '://' not in sub:
                    sub = 'http://' + sub
                if sub:
                    module = dict()
                    module["sub"] = sub
                    module["name"] = name
                    module["poc"] = exp
                    conf.queue.put(module)
    except FileNotFoundError:
        err_msg = "The %s was not found" % conf.INPUT_FILE_PATH
        sys.exit(outputscreen.error(err_msg))
    except:
        raise
        # err_msg = "又有bug了啊，我哭 QWQ"
        # sys.exit(outputscreen.error(err_msg))


# 加载指定代理IP
def load_proxy_ip():
    Hook = dict()
    if 'https' in conf.INPUT_TARGET_URL:
        Hook.update({"proxies": {'%s' % 'https': conf.INPUT_TARGET_PROXY}})
    else:
        Hook.update({"proxies": {'%s' % 'http': conf.INPUT_TARGET_PROXY}})
    conf.HOOK = Hook


# 随机从代理IP池中加载代理
def load_proxy_random_ip(scheme):
    Hook = dict()
    proxy_list = []
    with open(conf.PROXY_IP_PATH)as ppf:
        proxy_lines = ppf.readlines()
    for porxy_ip in proxy_lines:
        proxy_list.append(porxy_ip.strip())
    # print(random_proip)
    Hook.update({"proxies": {'%s' % scheme: random.choice(proxy_list)}})
    conf.HOOK = Hook
    # return conf.HOOK


# 加载指定的UA头
def load_ua():
    Hook = dict()
    Hook.update({"headers": {'User-Agent': conf.INPUT_TARGET_UA}})
    conf.HOOK = Hook


# 加载cookie
def load_cookie():
    Hook = dict()
    Hook.update({"headers": {'Cookie': conf.INPUT_TARGET_COOKIE}})
    # Hook.update({'Cookie': conf.INPUT_TARGET_COOKIE})
    conf.HOOK = Hook


# 加载API查询出的目标
def load_api_mode():
    conf.API_OUTPUT = os.path.join(paths.DATA_PATH, conf.API_MODE)
    if not os.path.exists(conf.API_OUTPUT):
        os.mkdir(conf.API_OUTPUT)
    output = conf.API_OUTPUT
    dork = conf.API_DORK
    limit = conf.API_LIMIT
    offset = conf.API_OFFSET
    if conf.API_MODE is 'Zoomeye':
        anslist = ZoomEyeSearch(query=dork, limit=limit, type=conf.ZOOMEYE_SEARCH_TYPE, offset=offset)
    if conf.API_MODE is 'Google':
        anslist = GoogleSearch(query=dork, limit=limit, offset=conf.API_OFFSET)
    if anslist:
        tmpIpFile = os.path.join(output, '%s.txt' % (time.strftime('%Y%m%d%H%M%S')))
        with open(tmpIpFile, 'w') as fp:
            for each in anslist:
                if isinstance(each, list):  # for ZoomEye web type
                    each = each[0]
                fp.write(each + '\n')
        with open(tmpIpFile)as tm:
            for target in tm.readlines():
                for name, exp in conf.MODULE_PLUGIN.items():
                    sub = target.strip()
                    if '://' not in sub:
                        sub = 'http://' + sub
                    if sub:
                        module = dict()
                        module["sub"] = sub
                        module["name"] = name
                        module["poc"] = exp
                        conf.queue.put(module)
    else:
        msg = '%s Api 未找到符合 %s 的目标' % (conf.API_MODE, dork)
        sys.exit(outputscreen.error(msg))


# 加载随机UA头
def loadfakeuseragent():
    """
    随机UA头
    :return:
    """
    ua_list = []
    ua_file = paths.UA_LIST_PATH
    if os.path.isfile(ua_file):
        with open(ua_file)as u:
            ua = u.readlines()
        for a in ua:
            a = a.strip()
            ua_list.append(a)
        return random.choice(ua_list)
    else:
        sys.exit(outputscreen.error('NO found %s' % ua_file))
