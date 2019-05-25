#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 16:46
# @Author  : Goop
# @Site    : 
# @File    : report.py
# @Software: PyCharm
class SetHtml():
    report_css = """<html>
<head>
<title>Charon Report</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style>
    body {width:960px; margin:auto; margin-top:10px; background:rgb(200,200,200);}
    p {color: #666;}
    h2 {color:#002E8C; font-size: 1em; padding-top:5px;}
    ul li {
    word-wrap: break-word;
    white-space: -moz-pre-wrap;
    white-space: pre-wrap;
    margin-bottom:10px;
    }
    a:link,a:visited{
    text-decoration:none;  /*超链接无下划线*/
    }
</style>
</head>
"""

    report_body = """<body>
<p>扫描完毕，请自行复测漏洞是否存在。  </p>
<p>整个扫描在 <b>{time:.2f}</b> 秒内完成.</p>

"""

    report_content = """
<h2>{vuln}</h2>
<ul>
{list}
</ul>
"""

    report_list = """
<li class="normal"> <a href="{url}" target="_blank">{text}</a></li>
"""
