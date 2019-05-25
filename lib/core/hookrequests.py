#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 12:12
# @Author  : Goop
# @Site    : 
# @File    : hookrequests.py
# @Software: PyCharm


from lib.core.data import HCONF
from requests.models import Request
from requests.sessions import Session
from requests.sessions import merge_setting, merge_cookies
from requests.cookies import RequestsCookieJar
from requests.utils import get_encodings_from_content
from urllib3 import disable_warnings


def session_request(self, method, url,
                    params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                    timeout=None,
                    allow_redirects=True, proxies=None, hooks=None, stream=None, verify=False, cert=None, json=None):
    # Create the Request.
    conf = HCONF.get("HOOK", {})
    # print("tttttttttttt", conf, '\n')
    if timeout is None and "timeout" in conf:
        timeout = conf["timeout"]
    merged_cookies = merge_cookies(merge_cookies(RequestsCookieJar(), self.cookies),
                                   cookies or (conf.cookie if 'cookie' in conf else None))

    req = Request(
        method=method.upper(),
        url=url,
        headers=merge_setting(headers, conf["headers"] if 'headers' in conf else {}),
        files=files,
        data=data or {},
        json=json,
        params=params or {},
        auth=auth,
        cookies=merged_cookies,
        hooks=hooks,
    )
    prep = self.prepare_request(req)

    proxies = proxies or (conf["proxies"] if 'proxies' in conf else {})

    settings = self.merge_environment_settings(
        prep.url, proxies, stream, verify, cert
    )

    # Send the request.
    send_kwargs = {
        'timeout': timeout,
        'allow_redirects': allow_redirects,
    }
    send_kwargs.update(settings)
    resp = self.send(prep, **send_kwargs)

    if resp.encoding == 'ISO-8859-1':
        encodings = get_encodings_from_content(resp.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = resp.apparent_encoding

        resp.encoding = encoding

    return resp


def patch_session():
    Session.request = session_request


def _disable_warnings():
    """
    Helper for quickly disabling all urllib3 warnings.
    """
    disable_warnings()
