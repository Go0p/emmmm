#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import requests
import getpass
import sys
import json
from lib.core.data import paths
from lib.core.setting import outputscreen
from lib.api.config.config import ConfigFileParser


class ZoomEye(object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

        self.token = ''
        self.zoomeye_login_api = "https://api.zoomeye.org/user/login"
        self.zoomeye_dork_api = "https://api.zoomeye.org/{}/search"

    def auto_login(self):
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        outputscreen.info(msg)
        try:
            self.username = ConfigFileParser().ZoomEyeEmail()
            self.password = ConfigFileParser().ZoomEyePassword()
        except:
            pass

        if bool(self.username and self.password):
            if self.get_token():
                return

        msg = 'Automatic authorization failed.'
        outputscreen.warning(msg)
        self.manual_login()

    def manual_login(self):
        msg = 'Please input your ZoomEye Email and Password below.'
        outputscreen.info(msg)
        try:
            from lib.core.data import conf, cmdLineOptions
            self.username = input('[!] ZoomEye Username(Email): ').strip()
            self.password = getpass.getpass(prompt='[!] ZoomEye Password: ').strip()
            # self.username = input('[!] ZoomEye Password: ').strip()
        except KeyboardInterrupt:
            sys.exit(outputscreen.nerror('User quit!'))
        self.get_token()
        if not self.get_token():
            msg = 'Invalid ZoomEye username or password.'
            sys.exit(outputscreen.error(msg))

    def get_token(self):
        # Please access https://www.zoomeye.org/api/doc#login
        # data = '{{"username": "{}", "password": "{}"}}'.format(self.username,self.password)
        data = {
            'username': self.username,
            'password': self.password
        }
        data = json.dumps(data)
        resp = requests.post(self.zoomeye_login_api, data=data, )
        if resp.status_code == 200 and 'access_token' in resp.text:
            self.token = json.loads(resp.text)['access_token']
            return self.token
        if resp.status_code == 400 and '400 Unknown Virtual Host' in resp.text:
            msg = '使用-As加载的脚本超过12个会有这个未知的bug，还不知道怎么解决QAQ,先使用-s吧。'
            sys.exit(outputscreen.error(msg))
        return False

    def setToken(self, token):
        """set Token from exist token string"""
        self.token = token.strip()

    def dork_search(self, dork, page=0, resource='web', facets=['ip']):
        """Search records with ZoomEye dorks.

        param: dork
               ex: country:cn
               access https://www.zoomeye.org/search/dorks for more details.
        param: page
               total page(s) number
        param: resource
               set a search resource type, ex: [web, host]
        param: facet
               ex: [app, device]
               A comma-separated list of properties to get summary information
        """
        result = []
        if isinstance(facets, (tuple, list)):
            facets = ','.join(facets)

        zoomeye_api = self.zoomeye_dork_api.format(resource)
        headers = {'Authorization': 'JWT %s' % self.token}
        params = {'query': dork, 'page': page + 1, 'facets': facets}
        resp = requests.get(zoomeye_api, params=params, headers=headers)

        if resp and resp.status_code == 200 and 'matches' in resp.json():
            matches = resp.json().get('matches')
            # total = resp.json().get('total')  # all matches items num
            result = matches

            # Every match item incudes the following information:
            # geoinfo
            # description
            # check_time
            # title
            # ip
            # site
            # system
            # headers
            # keywords
            # server
            # domains
        return result

    def resources_info(self):
        """Resource info shows us available search times.

        host-search: total number of available host records to search
        web-search: total number of available web records to search
        """
        data = None
        zoomeye_api = "https://api.zoomeye.org/resources-info"
        headers = {'Authorization': 'JWT %s' % self.token}
        resp = requests.get(zoomeye_api, headers=headers)
        if resp and resp.status_code == 200 and 'plan' in resp.json():
            data = resp.json()

        return data


def show_site_ip(data):
    if data:
        for i in data:
            print(i.get('site'), i.get('ip'))


def show_ip_port(data):
    if data:
        for i in data:
            print(i.get('ip'), i.get('portinfo').get('port'))
