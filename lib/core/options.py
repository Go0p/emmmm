#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/30 13:31
# @Author  : Goop
# @Site    : 
# @File    : options.py
# @Software: PyCharm


import sys
import os
import ipaddress
import time
from lib.core.data import conf, paths, cmdLineOptions, HCONF
from lib.core.setting import outputscreen


def initOptions(args):
    Misc(args)
    EngineRegister(args)
    TargetRegister(args)
    ScriptsRegister(args)
    ApiRegister(args)
    # ProxyRegister(args)
    HookRegister(args)
    OutPutRegister(args)
    # patch_session()
    # test(args)


def HookRegister(args):
    if args.proxy_ip:
        msg = 'Use proxy: %s' % args.proxy_ip
        outputscreen.info(msg)
        conf.PROXY_MODE = 'PROXY'
        conf.INPUT_TARGET_PROXY = args.proxy_ip
    elif args.proxy_pool_ip:
        proxy_pool_file = os.path.join(paths.DATA_PATH, 'Proxy_pool', 'proxy_pool.txt')
        if os.path.exists(proxy_pool_file):
            msg = 'Use proxy ip file: proxy_pool.txt'
            outputscreen.info(msg)
            conf.PROXY_MODE = "RANDOM_PROXY"
            conf.PROXY_IP_PATH = proxy_pool_file
        else:
            outputscreen.error("读取代理文件出错，请确保代理文件名为proxy_pool.txt,每行一条代理，格式如: 124.225.223.101:80")
            sys.exit()
    else:
        conf.PROXY_MODE = ''
    if args.user_agent:
        msg = "Use User-Agent: %s" % args.user_agent
        outputscreen.info(msg)
        conf.UA_MODE = 'UA'
        conf.INPUT_TARGET_UA = args.user_agent
    else:
        conf.UA_MODE = ''
    if args.set_cookie:
        msg = "Use Cookie: %s" % args.set_cookie
        outputscreen.info(msg)
        conf.COOKIE_MODE = 'COOKIE'
        conf.INPUT_TARGET_COOKIE = args.set_cookie
    else:
        conf.COOKIE_MODE = ''
    #     conf.INPUT_TARGET_PROXY = ''
    #     conf.PROXY_IP_PATH = ''


def EngineRegister(args):
    """
    加载并发引擎模块,-eT 多线程  -eG 协程
    :param args:
    :return:
    """
    thread_status = args.engine_thread
    if thread_status:
        conf.thread_mode = thread_status
    else:
        conf.thread_mode = False
    gevent_status = args.engine_gevent
    if gevent_status:
        conf.gevent_mode = gevent_status
    else:
        conf.gevent_mode = False
    if args.thread_num > 200 or args.thread_num < 1:
        msg = 'Invalid input in [-t](range: 1 to 200), has changed to default(30)'
        outputscreen.warning(msg)
        conf.thread_num = 10
        return
    conf.thread_num = args.thread_num


def TargetRegister(args):
    """
    加载目标
    :param args:
    :return:
    """
    msg = 'Initialize targets...'
    outputscreen.warning(msg)
    # 单一目标
    if args.target_single:
        msg = 'Load target: %s' % args.target_single
        outputscreen.info(msg)
        conf.TARGET_MODE = 'SINGLE'
        conf.INPUT_TARGET_URL = args.target_single
    # 目标为文件
    elif args.target_file:
        msg = 'Load targets from: %s' % args.target_file
        outputscreen.info(msg)
        conf.TARGET_MODE = 'FILE'
        conf.INPUT_FILE_PATH = args.target_file
    # 目标为Zoomeye搜索后的IP或web
    elif args.zoomeye_dork:
        msg = 'Load targets from Zoomeye_Api: %s' % args.zoomeye_dork
        outputscreen.info(msg)
        conf.TARGET_MODE = 'API'
        conf.API_MODE = 'Zoomeye'
        conf.API_DORK = args.zoomeye_dork
    elif args.google_dork:
        msg = 'Load targets from Google_Api: %s' % args.google_dork
        outputscreen.info(msg)
        conf.TARGET_MODE = 'API'
        conf.API_MODE = 'Google'
        conf.API_DORK = args.google_dork
    # 目标为IP段
    else:
        err_msg = 'No target or target file is specified!'
        outputscreen.error(err_msg)
        sys.exit()


def ScriptsRegister(args):
    script_name = args.script_name
    all_scripts = args.all_scripts
    pocs_path = paths.POCS_PATH
    # 存放脚本文件名
    script_name_list = []
    # 存放脚本文件路径
    script_path_list = []
    # 判断script是否存在，不存在为0
    flag = 0
    # script列表的长度,flag=len_script_name时退出查找文件的循环
    len_script_name = len(script_name)
    if not (script_name or all_scripts):
        err_msg = 'Use -s/-As load script/scripts'
        outputscreen.error(err_msg)
        sys.exit()
    # 设置单个或多个poc的路径，type(script_name)=list
    if script_name:
        for root, dirs, files in os.walk(pocs_path):
            """
                root ：所指的是当前正在遍历的目录的地址
                dirs ：当前文件夹中所有目录名字的 list (不包括子目录)
                files ：当前文件夹中所有的文件 (不包括子目录中的文件)
            """
            for file in files:
                # 文件名
                file_name = os.path.splitext(file)[0]
                # 文件后缀
                file_suffix = os.path.splitext(file)[1]
                # 路径
                file_path = os.path.join(root, file)
                file_abs_path = os.path.abspath(file)
                # 文件父目录
                file_parent = os.path.dirname(file_path)

                # print("file : {0}".format(file))
                # print("file_name : {0}".format(file_name))
                # # print("file_suffix : {0}".format(file_suffix))
                # print("file_path : {0}".format(file_path))
                # # print("file_parent : {0}".format(file_parent))

                for target_file in script_name:
                    if target_file == file_name:
                        flag += 1
                        script_name_list.append(file_name)
                        script_path_list.append(file_path)
            if flag == len_script_name:
                break
            conf.MODULE_NAME = script_name_list
            conf.MODULE_FILE_PATH = script_path_list
            # print('flagxxxxxxxxxxxxx',flag)
        if flag == 0:
            outputscreen.error('Script not %s exist, please check spelling' % script_name)
            sys.exit()
        else:
            msg = 'Load script:%s' % conf.MODULE_NAME
            outputscreen.info(msg)
    # 同种类型下的所有poc，eg.struts2_all包含003-053的全部poc
    if all_scripts:
        for root, dirs, files in os.walk(pocs_path):
            for di in dirs:
                if all_scripts == di:
                    file_path = os.path.join(root, di)
                    file_name_list = list(
                        map(lambda filename: '{}'.format(filename),
                            filter(lambda filename: False if '__' in filename else True, os.listdir(file_path))))
                    for sn in file_name_list:
                        if sn[-3:] == '.py':
                            script_name_list.append(sn)
                    for file_name in file_name_list:
                        script_path = os.path.join(file_path, file_name)
                        # print('script_path', script_path)
                        flag += 1
                        if file_name[-3:] == '.py':
                            script_path_list.append(script_path)
                    conf.MODULE_NAME = script_name_list
                    conf.MODULE_FILE_PATH = script_path_list
        if flag == 0:
            outputscreen.error('File not %s exist. please check spelling' % all_scripts)
            sys.exit()
        else:
            msg = 'Load script:%s' % conf.MODULE_NAME
            outputscreen.info(msg)


def ApiRegister(args):
    search_type = args.search_type
    google_proxy = args.google_proxy
    api_limit = args.api_limit
    offset = args.api_offset
    if not 'API_MODE' in conf:
        return
    if not conf.API_DORK:
        msg = 'Empty API dork, show usage with [-h]'
        sys.exit(outputscreen.error(msg))

    if offset < 0:
        msg = 'Invalid value in [--offset], show usage with [-h]'
        sys.exit(outputscreen.error(msg))
    else:
        conf.API_OFFSET = offset
    if api_limit <= 0:
        msg = 'Invalid value in [--limit], show usage with [-h]'
        sys.exit(outputscreen.error(msg))
    else:
        conf.API_LIMIT = api_limit
    if conf.API_MODE is 'Zoomeye':
        if search_type not in ['web', 'host']:
            msg = 'Invalid value in [--search-type], show usage with [-h]'
            sys.exit(outputscreen.error(msg))
        else:
            conf.ZOOMEYE_SEARCH_TYPE = search_type

    elif conf.API_MODE is 'Google':
        conf.GOOGLE_PROXY = google_proxy


def OutPutRegister(args):
    output_name = args.output_name
    conf.OUT_FILE_STATUS = args.output_file_status
    if conf.OUT_FILE_STATUS:
        if output_name:
            output_path = os.path.join(paths.OUTPUT_PATH, output_name)
            conf.OUT_FILE_NAME = output_path + '.html'
        else:
            file_name = '{}'.format("report-" + time.strftime("%Y-%m-%d", time.localtime()))
            output_path = os.path.join(paths.OUTPUT_PATH, file_name)
            conf.OUT_FILE_NAME = output_path + '.html'


def Misc(args):
    script_name_list = []
    pocs_path = paths.POCS_PATH
    if args.show_scripts:
        for root, dirs, files in os.walk(pocs_path):
            for di in dirs:
                file_path = os.path.join(root, di)
                file_name_list = list(
                    map(lambda filename: '{}'.format(filename),
                        filter(lambda filename: False if '__' in filename else True, os.listdir(file_path))))
                for sn in file_name_list:
                    if sn[-3:] == '.py':
                        script_name_list.append(sn)
        outputscreen.success('Poc Total:%s' % len(script_name_list) + '\n')
        for name in script_name_list:
            outputscreen.success(name)
        exit()
