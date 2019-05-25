#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import sys
import socket
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as ServerHttpDenied
from googleapiclient.errors import UnknownApiNameOrVersion as ApiNameOrVersion
from lib.api.config.config import ConfigFileParser
from lib.core.data import conf
from lib.core.setting import outputscreen
from httplib2 import Http, ProxyInfo
from socket import error as SocketError

timeout = 20
socket.setdefaulttimeout(timeout)


class PROXY_TYPE:  # keep same with SocksiPy(import socks)
    PROXY_TYPE_SOCKS4 = SOCKS4 = 1
    PROXY_TYPE_SOCKS5 = SOCKS5 = 2
    PROXY_TYPE_HTTP = HTTP = 3
    PROXY_TYPE_HTTP_NO_TUNNEL = 4


def _initHttpClient():
    if conf.GOOGLE_PROXY:
        proxy_str = conf.GOOGLE_PROXY
    elif ConfigFileParser().GoogleProxy():
        proxy_str = ConfigFileParser().GoogleProxy()
    else:
        proxy_str = None

    if not proxy_str:
        return Http()

    msg = 'Proxy: %s' % proxy_str
    outputscreen.info(msg)
    proxy = proxy_str.strip().split(' ')
    if len(proxy) != 3:
        msg = 'SyntaxError in GoogleProxy string, Please check your args or config file.'
        sys.exit(outputscreen.error(msg))
    if proxy[0].lower() == 'http':
        type = PROXY_TYPE.HTTP
    elif proxy[0].lower() == 'sock5':
        type = PROXY_TYPE.SOCKS5
    elif proxy[0].lower() == 'sock4':
        type = PROXY_TYPE.SOCKS4
    else:
        msg = 'Invalid proxy-type in GoogleProxy string, Please check your args or config file.'
        sys.exit(outputscreen.error(msg))
    try:
        port = int(proxy[2])
    except ValueError:
        msg = 'Invalid port in GoogleProxy string, Please check your args or config file.'
        sys.exit(outputscreen.error(msg))
    else:
        http_client = Http(proxy_info=ProxyInfo(type, proxy[1], port))
    return http_client


def GoogleSearch(query, limit, offset=0):
    key = ConfigFileParser().GoogleDeveloperKey()
    engine = ConfigFileParser().GoogleEngine()
    if not key or not engine:
        msg = "Please config your 'developer_key' and 'search_enging' at toolkit.conf"
        sys.exit(outputscreen.error(msg))
    try:
        service = build("customsearch", "v1", http=_initHttpClient(), developerKey=key)

        result_info = service.cse().list(q=query, cx=engine).execute()
        msg = 'Max query results: %s' % str(result_info.get('searchInformation', {}).get('totalResults'))
        outputscreen.info(msg)

        ans = list()
        limit += offset
        for i in range(int(offset / 10), int((limit + 10 - 1) / 10)):
            result = service.cse().list(q=query, cx=engine, num=10, start=i * 10 + 1).execute()
            if 'items' in result:
                for url in result.get('items'):
                    ans.append(url.get('link'))
        return ans
    except SocketError:
        sys.exit(outputscreen.error('Unable to connect Google, maybe agent/proxy error.'))
    except ApiNameOrVersion:
        msg = '使用-As加载的脚本超过12个会有这个未知的bug，还不知道怎么解决QAQ,先使用-s吧。'
        sys.exit(outputscreen.error(msg))
    except ServerHttpDenied:
        outputscreen.warning('It seems like Google-Server denied this request.')
        sys.exit()
