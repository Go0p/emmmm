#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/14 上午2:07
# @Author  : SecPlus
# @Site    : www.SecPlus.org
# @Email   : TideSecPlus@gmail.com

# 2018.04.14 结合wdscan和其他爬虫，相对比较完善的spider

import random
import re, requests
import time

import sys


def url_protocol(url):
    domain = re.findall(r'.*(?=://)', url)
    if domain:
        return domain[0]
    else:
        return url


def same_url(urlprotocol, url):
    url = url.replace(urlprotocol + '://', '')
    if re.findall(r'^www', url) == []:
        sameurl = 'www.' + url
        if sameurl.find('/') != -1:
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
        else:
            sameurl = sameurl + '/'
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    else:
        if url.find('/') != -1:
            sameurl = 'www.' + re.findall(r'(?<=www.).*?(?=/)', url)[0]
        else:
            sameurl = url + '/'
            sameurl = 'www.' + re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    print('the domain is：' + sameurl)
    return sameurl


def requests_headers():
    '''
    Random UA  for every requests && Use cookie to scan
    '''
    user_agent = ['Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre',
                  'Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60',
                  'Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5']
    UA = random.choice(user_agent)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': UA, 'Upgrade-Insecure-Requests': '1', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
        'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8',
        "Referer": "http://www.baidu.com/link?url=www.so.com&url=www.soso.com&&url=www.sogou.com"}
    return headers


class linkQuence:
    def __init__(self):
        self.visited = []  # 已访问过的url初始化列表
        self.unvisited = []  # 未访问过的url初始化列表
        self.external_url = []  # 外部链接

    def getVisitedUrl(self):  # 获取已访问过的url
        return self.visited

    def getUnvisitedUrl(self):  # 获取未访问过的url
        return self.unvisited

    def getExternal_link(self):
        return self.external_url  # 获取外部链接地址

    def addVisitedUrl(self, url):  # 添加已访问过的url
        return self.visited.append(url)

    def addUnvisitedUrl(self, url):  # 添加未访问过的url
        if url != '' and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0, url)

    def addExternalUrl(self, url):  # 添加外部链接列表
        if url != '' and url not in self.external_url:
            return self.external_url.insert(0, url)

    def removeVisited(self, url):
        return self.visited.remove(url)

    def popUnvisitedUrl(self):  # 从未访问过的url中取出一个url
        try:  # pop动作会报错终止操作，所以需要使用try进行异常处理
            return self.unvisited.pop()
        except:
            return None

    def unvisitedUrlEmpty(self):  # 判断未访问过列表是不是为空
        return len(self.unvisited) == 0


class Spider():
    '''
    真正的爬取程序
    '''

    def __init__(self, url, domain_url, urlprotocol):
        self.linkQuence = linkQuence()  # 引入linkQuence类
        self.linkQuence.addUnvisitedUrl(url)  # 并将需要爬取的url添加进linkQuence对列中
        self.current_deepth = 1  # 设置爬取的深度
        self.domain_url = domain_url
        self.urlprotocol = urlprotocol

    def getPageLinks(self, url):
        '''
            获取页面中的所有链接
        '''
        try:
            headers = requests_headers()
            content = requests.get(url, timeout=5, headers=headers, verify=False).text.encode('utf-8')
            links = []
            tags = ['a', 'A', 'link', 'script', 'area', 'iframe', 'form']  # img
            tos = ['href', 'src', 'action']
            if url[-1:] == '/':
                url = url[:-1]
            try:
                for tag in tags:
                    for to in tos:
                        link1 = re.findall(r'<%s.*?%s="(.*?)"' % (tag, to), str(content))
                        link2 = re.findall(r'<%s.*?%s=\'(.*?)\'' % (tag, to), str(content))
                        for i in link1:
                            links.append(i)

                        for i in link2:
                            if i not in links:
                                links.append(i)

            except:
                print('[!] Get link error')
                pass
            return links
        except:
            return []

    def getPageLinks_bak(self, url):
        '''
        获取页面中的所有链接
        '''
        try:

            # pageSource=urllib2.urlopen(url).read()
            headers = requests_headers()
            time.sleep(0.5)
            pageSource = requests.get(url, timeout=5, headers=headers).text.encode('utf-8')
            pageLinks = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')', pageSource)
            # print pageLinks
        except:
            # print ('open url error')
            return []
        return pageLinks

    def processUrl(self, url):
        '''
        判断正确的链接及处理相对路径为正确的完整url
        :return:
        '''
        true_url = []
        in_link = []
        excludeext = ['.zip', '.rar', '.pdf', '.doc', '.xls', '.jpg', '.mp3', '.mp4', '.png', '.ico', '.gif', '.svg',
                      '.jpeg', '.mpg', '.wmv', '.wma', 'mailto', 'javascript', 'data:image']
        for suburl in self.getPageLinks(url):
            exit_flag = 0
            for ext in excludeext:
                if ext in suburl:
                    print("break:" + suburl)
                    exit_flag = 1
                    break
            if exit_flag == 0:
                if re.findall(r'/', suburl):
                    if re.findall(r':', suburl):
                        true_url.append(suburl)
                    else:
                        true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)
                else:
                    true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)

        for suburl in true_url:
            print('from:' + url + ' get suburl：' + suburl)

        return true_url

    def sameTargetUrl(self, url):
        same_target_url = []
        for suburl in self.processUrl(url):
            if re.findall(self.domain_url, suburl):
                same_target_url.append(suburl)
            else:
                self.linkQuence.addExternalUrl(suburl)
        return same_target_url

    def unrepectUrl(self, url):
        '''
        删除重复url
        '''
        unrepect_url = []
        for suburl in self.sameTargetUrl(url):
            if suburl not in unrepect_url:
                unrepect_url.append(suburl)
        return unrepect_url

    def crawler(self, crawl_deepth=1):
        '''
        正式的爬取，并依据深度进行爬取层级控制
        '''
        self.current_deepth = 0
        print("current_deepth:", self.current_deepth)
        while self.current_deepth < crawl_deepth:
            if self.linkQuence.unvisitedUrlEmpty(): break
            links = []
            while not self.linkQuence.unvisitedUrlEmpty():
                visitedUrl = self.linkQuence.popUnvisitedUrl()
                if visitedUrl is None or visitedUrl == '':
                    continue
                print("#" * 30 + visitedUrl + " :begin" + "#" * 30)
                for sublurl in self.unrepectUrl(visitedUrl):
                    links.append(sublurl)
                # links = self.unrepectUrl(visitedUrl)
                self.linkQuence.addVisitedUrl(visitedUrl)
                print("#" * 30 + visitedUrl + " :end" + "#" * 30 + '\n')
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            self.current_deepth += 1
        # print(self.linkQuence.visited)
        # print (self.linkQuence.unvisited)
        urllist = []
        urllist.append("#" * 30 + ' VisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getVisitedUrl():
            urllist.append(suburl)
        urllist.append('\n' + "#" * 30 + ' UnVisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getUnvisitedUrl():
            urllist.append(suburl)
        urllist.append('\n' + "#" * 30 + ' External_link ' + "#" * 30)
        for sublurl in self.linkQuence.getExternal_link():
            urllist.append(sublurl)
        urllist.append('\n' + "#" * 30 + ' Active_link ' + "#" * 30)
        actives = ['?', '.asp', '.jsp', '.php', '.aspx', '.do', '.action']
        active_urls = []
        for sublurl in urllist:
            for active in actives:
                if active in sublurl:
                    active_urls.append(sublurl)
                    break
        for active_url in active_urls:
            urllist.append(active_url)
        return urllist


def writelog(log, urllist):
    filename = log
    outfile = open(filename, 'w')
    for suburl in urllist:
        outfile.write(suburl + '\n')
    outfile.close()


def urlspider(rooturl, crawl_deepth=3):
    # ext_link = []
    urlprotocol = url_protocol(url)
    domain_url = same_url(urlprotocol, url)
    print("domain_url:" + domain_url)
    spider = Spider(url, domain_url, urlprotocol)
    urllist = spider.crawler(crawl_deepth)
    writelog(domain_url, urllist)
    print('-' * 20 + url + '-' * 20)
    for sublurl in urllist:
        print(sublurl)
    print('\n' + 'Result record in:' + domain_url + '.txt')


def SRC_spider(url, log, crawl_deepth=3):
    # url = 'http://2014.liaocheng.gov.cn'

    urlprotocol = url_protocol(url)
    domain_url = same_url(urlprotocol, url)
    print("domain_url:" + domain_url)
    spider = Spider(url, domain_url, urlprotocol)
    urllist = spider.crawler(crawl_deepth)
    writelog(log, urllist)
    print('-' * 20 + url + '-' * 20)
    # for sublurl in urllist:
    #     print sublurl
    print('\n' + 'Result record in:' + log)


if __name__ == '__main__':
    url = 'http://www.wuhubtv.com'
    craw_deepth = 5
    usage = '''
        python spider_v3.py  url  5   --> url为待爬取的网站地址，5为爬取深度，可以不设，默认为5。
        '''
    try:
        if len(sys.argv) == 2:
            url = sys.argv[1]
            craw_deepth = 5
        elif len(sys.argv) == 3:
            url = sys.argv[1]
            craw_deepth = int(sys.argv[2])
        else:
            print(usage)
            exit(0)

        urlprotocol = url_protocol(url)
        domain_url = same_url(urlprotocol, url)
        print("domain_url:" + domain_url)
        spider = Spider(url, domain_url, urlprotocol)
        urllist = spider.crawler(craw_deepth)
        writelog(domain_url + '.txt', urllist)
        # print urllist
        print('-' * 20 + url + '-' * 20)
        for sublurl in urllist:
            print(sublurl)
        print(len(urllist))
        print('\n' + 'Result record in:' + domain_url + '.txt')
    except:
        pass
