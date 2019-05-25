#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/7 16:17
# @Author  : Goop
# @Site    : 
# @File    : config.py
# @Software: PyCharm

import configparser
from lib.core.data import paths
from lib.core.setting import outputscreen


class ConfigFileParser:
    @staticmethod
    def _get_option(section, option):
        try:
            cf = configparser.ConfigParser()
            cf.read('E://Goop//toolkit.conf')
            # cf.read(paths.CONFIG_PATH)
            return cf.get(section=section, option=option)
        except configparser.NoOptionError:
            outputscreen.warning('Missing essential options, please check your config-file.')
            return ''

    def ZoomEyeEmail(self):
        return self._get_option('zoomeye', 'email')

    def ZoomEyePassword(self):
        return self._get_option('zoomeye', 'password')

    def CEyeToken(self):
        return self._get_option('ceye', 'token')

    def GoogleProxy(self):
        return self._get_option('google', 'proxy')

    def GoogleDeveloperKey(self):
        return self._get_option('google', 'developer_key')

    def GoogleEngine(self):
        return self._get_option('google', 'search_engine')

    def FofaEmail(self):
        return self._get_option('fofa', 'email')

    def FofaKey(self):
        return self._get_option('fofa', 'api_key')
