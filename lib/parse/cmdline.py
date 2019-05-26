#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 23:18
# @Author  : Goop
# @Site    : 
# @File    : cmdline.py
# @Software: PyCharm
import argparse
import sys


def cmdLineParser():
    parser = argparse.ArgumentParser(usage='python3 Charon.py -iU/-iF url/file -s/-As load scripts')

    engine = parser.add_argument_group('Engine')

    # engine.add_argument('-t', '--thread', dest="thread_num", type=int, default=10,
    #                     help='num of threads, 10 by default')
    engine.add_argument('-eT', dest="engine_thread", default=False, action='store_true',
                        help='Multi-Threaded engine (default choice)')

    engine.add_argument('-eG', dest="engine_gevent", default=False, action='store_true',
                        help='Gevent engine (single-threaded with asynchronous)')

    engine.add_argument('-t', metavar='NUM', dest="thread_num", type=int, default=10,
                        help='num of threads/concurrent, 10 by default')
    target = parser.add_argument_group('Target')

    target.add_argument('-iU', metavar='TARGET', dest="target_single", type=str, default='',
                        help="scan a single target ")
    target.add_argument('-iF', metavar='FILE', dest="target_file", type=str, default='',
                        help='load targets from targetFile ')

    script = parser.add_argument_group('Scripts')

    script.add_argument('-s', dest="script_name", type=str, nargs='+', default=[],
                        help="select the scripts to check")
    script.add_argument('-As', dest="all_scripts", type=str, default='',
                        help="All scripts of the same type")

    output = parser.add_argument_group('Output')

    output.add_argument('-oF', metavar='FILE-NAME', dest="output_name", type=str, default='',
                        help='output file path&name. default in ./output/')
    output.add_argument('-sF', '--skip-outfile', dest="output_file_status", default=True, action='store_false',
                        help='disable file output')
    proxy = parser.add_argument_group('Proxy')

    proxy.add_argument('-pI', metavar='PROXY', dest="proxy_ip", type=str, default='',
                       help="Select a proxy IP (e.g. -pI '127.0.0.1:8080')")
    proxy.add_argument('-pL', metavar='PROXY_POOL', dest="proxy_pool_ip", type=bool, default=False,
                       help='Select one at random from the proxy pool (e.g. -pL True)')
    header = parser.add_argument_group('Headers')
    header.add_argument('-uA', metavar='User-Agent', dest="user_agent", type=str, default='',
                        help="Select a User-Agent (e.g. -uA 'Hello Charon!')")
    header.add_argument('-uC', metavar='COOKIE', dest="set_cookie", type=str, default='',
                        help="Add a Cookie (e.g. -uC 'ASPSESSION:XXXXXX')")

    api = parser.add_argument_group('Api')
    api.add_argument('-aZ', '--zoomeye', metavar='DORK', dest="zoomeye_dork", type=str, default='',
                     help='ZoomEye dork (e.g. "zabbix port:8080")')
    api.add_argument('-aS', '--shodan', metavar='DORK', dest="shodan_dork", type=str, default='',
                     help='Shodan dork.')
    api.add_argument('-aG', '--google', metavar='DORK', dest="google_dork", type=str, default='',
                     help='Google dork (e.g. "inurl:admin.php")')
    api.add_argument('-aF', '--fofa', metavar='DORK', dest="fofa_dork", type=str, default='',
                     help='FoFa dork (e.g. "banner=users && protocol=ftp")')
    api.add_argument('--limit', metavar='NUM', dest="api_limit", type=int, default=10,
                     help='Maximum searching results (default:10)')
    api.add_argument('--offset', metavar='OFFSET', dest="api_offset", type=int, default=0,
                     help="Search offset to begin getting results from (default:0)")
    api.add_argument('--search-type', metavar='TYPE', dest="search_type", action="store", default='host',
                     help="[ZoomEye] search type used in ZoomEye API, web or host (default:host)")
    api.add_argument('--gproxy', metavar='PROXY', dest="google_proxy", action="store", default=None,
                     help="[Google] Use proxy for Google (e.g. \"sock5 127.0.0.1 7070\" or \"http 127.0.0.1 1894\"")

    misc = parser.add_argument_group('Misc')
    misc.add_argument('--timeout', dest="timeout", default=1, type=int,
                      help='Sets the timeout for network requests')
    misc.add_argument('--show', dest="show_scripts", default=False, action='store_true',
                      help='show available script names in .poc and exit')
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    # return vars(args)
    return args


if __name__ == "__main__":
    a = cmdLineParser()
    print(a)
