#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/30 12:23
# @Author  : Goop
# @Site    : 
# @File    : engine.py
# @Software: PyCharm


import threading
import time
import os
import traceback
# from urllib3 import disable_warnings
import warnings
import sys
from lib.core.data import conf, paths, th
from lib.core.setting import outputscreen
from lib.core.report import SetHtml

warnings.filterwarnings("ignore")


# disable_warnings()


def initEngine():
    # init control parameter
    th.result = ''
    th.thread_count = th.thread_num = conf.thread_num
    th.thread_mode = conf.thread_mode
    th.target = conf.queue
    th.s_flag = True
    # 是否继续扫描标志位
    th.is_continue = True
    # 控制台宽度
    th.console_width = 100
    # 记录开始时间
    th.start_time = time.time()
    setThreadLock()
    th.scan_count = th.found_count = 0
    msg = 'Set the number of thread: %d' % th.thread_num
    outputscreen.info(msg)


def setThreadLock():
    if th.thread_mode:
        th.found_count_lock = threading.Lock()
        th.scan_count_lock = threading.Lock()
        th.thread_count_lock = threading.Lock()
        th.proxy_random_lock = threading.Lock()
        th.output_lock = threading.Lock()
        th.file_lock = threading.Lock()
        th.load_lock = threading.Lock()


def scan():
    while True:
        if th.thread_mode: th.load_lock.acquire()
        if th.target.qsize() > 0 and th.is_continue:
            module = th.target.get(timeout=1.0)
            target = module["sub"]
            name = module["name"]
            if conf.PROXY_MODE == 'RANDOM_PROXY':
                from .loader import load_proxy_random_ip
                if 'https' in target:
                    th.proxy_random_lock.acquire()
                    load_proxy_random_ip('https')
                    th.proxy_random_lock.release()
                else:
                    th.proxy_random_lock.acquire()
                    load_proxy_random_ip('http')
                    th.proxy_random_lock.release()
            if '.py' in name:
                name = module["name"][:-3]
            else:
                name = module["name"]
            module_obj = module["poc"]
            if th.thread_mode:
                th.load_lock.release()
        else:
            if th.thread_mode:
                th.load_lock.release()
            break
        try:
            # 对每个target进行检测
            status = module_obj.poc(target)
            setreturn(status, target, name)
        except:
            # 抛出异常时，添加errmsg键值
            th.errmsg = traceback.format_exc()
            th.is_continue = False
        # 多线程模式下需要加锁，解锁
        if th.thread_mode:
            th.scan_count_lock.acquire()
        th.scan_count += 1
        if th.thread_mode:
            th.scan_count_lock.release()
        if th.s_flag:
            printProgress()
    if th.s_flag:
        printProgress()
    if th.thread_mode: th.thread_count_lock.acquire()
    th.thread_count += -1
    if th.thread_mode: th.thread_count_lock.release()


def run():
    initEngine()
    # 多线程模式
    if conf.thread_mode:
        outputscreen.info('Threading mode')
        for i in range(th.thread_num):
            t = threading.Thread(target=scan, name=str(i))
            t.setDaemon(True)
            t.start()
            # It can quit with Ctrl-C
        try:
            while 1:
                if th.thread_count > 0 and th.is_continue:
                    time.sleep(0.01)
                else:
                    break
        except KeyboardInterrupt as e:
            outputscreen.nerror('User quit!')
            th.is_continue = False
    # 协程模式
    elif conf.gevent_mode:
        from gevent import monkey
        monkey.patch_all()
        import gevent
        outputscreen.info('Coroutine mode')
        while th.target.qsize() > 0 and th.is_continue:
            try:
                gevent.joinall([gevent.spawn(scan) for i in range(0, th.thread_num) if th.target.qsize() > 0])
            except KeyboardInterrupt:
                sys.exit(outputscreen.error('Ctrl+C quit!'))
        #     th.is_continue = False
    # except KeyboardInterrupt:
    #     sys.exit(outputscreen.error('[-] Ctrl+C quit!'))
    if 'errmsg' in th:
        outputscreen.error(th.errmsg)


def setreturn(status, url, vuln):
    def printScrren(msg):
        if th.s_flag:
            if th.thread_mode: th.output_lock.acquire()
            outputscreen.ensuccess('\r' + msg + '\n\r')
            if th.thread_mode: th.output_lock.release()
        if th.s_flag and conf.OUT_FILE_STATUS:
            output2file(msg, url, vuln)

    if status:
        if type(status) == set:
            for x in status:
                printScrren('[Success] ' + str(x))
        elif type(status) == list:
            for x in status:
                printScrren('[Success] ' + str(x))
        else:
            msg = str(status)
            printScrren('[Success] ' + msg)
        if th.thread_mode: th.found_count_lock.acquire()
        th.found_count += 1
        if th.thread_mode: th.found_count_lock.release()


def printProgress():
    msg = '[结果] 发现 %s | 剩余 %s | 探测的 %s 个在 %.2f 秒内' % (
        th.found_count, th.target.qsize(), th.scan_count, time.time() - th.start_time)
    out = '\r' + msg
    if th.thread_mode: th.output_lock.acquire()
    outputscreen.Progress(out)
    if th.thread_mode: th.output_lock.release()


def output2file(result, url, vuln):
    body = SetHtml.report_body.format(time=time.time() - th.start_time)
    # html = SetHtml.report_css + body
    file_name = conf.OUT_FILE_NAME
    if th.thread_mode: th.file_lock.acquire()
    if not os.path.exists(file_name):
        f = open(file_name, 'a', encoding="utf-8")
        f.write(SetHtml.report_css + body)
        f.close()

        l = SetHtml.report_list.format(url=url, text=result)
        content = SetHtml.report_content.format(vuln=vuln, list=l)
        f2 = open(file_name, 'a', encoding="utf-8")
        f2.write(content)
        f2.close()
    else:
        l = SetHtml.report_list.format(url=url, text=result)
        content = SetHtml.report_content.format(vuln=vuln, list=l)
        f2 = open(file_name, 'a', encoding="utf-8")
        f2.write(content)
        f2.close()
    if th.thread_mode: th.file_lock.release()
