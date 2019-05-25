import requests
from lib.core.setting import url200or404Check

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
paths = ['/ws_utc/config.do', '/ws_utc/begin.do'
         ]


def poc(url):
    proxies = {'http': '127.0.0.1:9999'}
    for path in paths:
        url1 = "%s%s" % (url, path)
        result = "目标Weblogic可能存在任意文件上传漏洞,CVE-2018-2894 : %s" % url1
        timeout = 5
        try:
            req = requests.get(url1, headers=headers, timeout=timeout, )
            if (req.status_code == 200 and url200or404Check(url1)) and (
                    'label_setting_menu_item_general'.lower() in str(req.text).lower()):
                return result
        except:
            pass


if __name__ == "__main__":
    a = poc('http://192.168.106.130:7001')
    print(a)
