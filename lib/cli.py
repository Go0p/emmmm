#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 23:19
# @Author  : Goop
# @Site    : 
# @File    : cli.py
# @Software: PyCharm

import os
import sys
from lib.core.setting import banner, setPaths
from lib.parse.cmdline import cmdLineParser
from lib.core.data import cmdLineOptions, paths, conf, th, HCONF
from lib.core.hookrequests import patch_session,_disable_warnings
from lib.core.options import initOptions
from lib.core.setting import outputscreen
from lib.scheduler.engine import run
from lib.scheduler.loader import loadPayload, setModule


def module_path():
    """
    This will get us the program's directory
    """
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def check_environment():
    try:
        os.path.isdir(module_path())
    except Exception:
        err_msg = "your system does not properly handle non-ASCII paths. "
        err_msg += "Please move the pocsuite's directory to the other location"
        outputscreen.error(err_msg)
        raise SystemExit


def main():
    check_environment()
    paths.ROOT_PATH = module_path()
    setPaths()
    try:
        banner()
        cmdLineOptions.update(cmdLineParser().__dict__)
        initOptions(cmdLineOptions)
    except:
        err_msg = 'I think you entered the wrong parameter...'
        sys.exit(outputscreen.error(err_msg))

    try:
        loadPayload()
        setModule()
        patch_session()
        _disable_warnings()
        # print('cmdLineOptions', cmdLineOptions, '\n')
        # print('conf', conf, '\n')
    except AttributeError:
        raise
        # print('xxxxxxxxxx')
        # exit()

    run()
    if th.found_count and conf.OUT_FILE_STATUS:
        outputscreen.resuccess('Report generated successfully -> %s' % conf.OUT_FILE_NAME)
    else:
        outputscreen.nerror('本次扫描未产生报告')


if __name__ == "__main__":
    main()
