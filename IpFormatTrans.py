#!/usr/bin/python
# -*- coding: UTF-8 -*-

import struct
import socket

class IpFormatTrans():

    def __init__(self):
        pass

    @staticmethod
    def ip_ntop(ip_str):
        if ip_str is None or len(ip_str) == 0:
            return ""

        if ip_str[0] == "-":
            #ipv6
            high = long(ip_str[1:].split(".")[0])
            low = long(ip_str[1:].split(".")[1])

            high1 = socket.htonl(int(high >> 32))
            high2 = socket.htonl(int(high << 32 >> 32))

            low1 = socket.htonl(int(low >> 32))
            low2 = socket.htonl(int(low << 32 >> 32))

            return socket.inet_ntop(socket.AF_INET6, struct.pack('IIII', high1, high2, low1, low2))
        else:
            #ipv4
            return socket.inet_ntoa(struct.pack('I',socket.htonl(int(ip_str.split(".")[0]))))

    @staticmethod
    def ip_pton(ip_str):
        if ip_str is None or len(ip_str) == 0:
            return ""

        if ip_str.find(":") == -1:
            #ipv4
            return socket.ntohl(struct.unpack("I", socket.inet_pton(socket.AF_INET, ip_str))[0])
        else:
            #ipv6
            ip_bytes = socket.inet_pton(socket.AF_INET6, ip_str)

            high1, high2, low1, low2 = struct.unpack("IIII", ip_bytes)
            high1 = socket.ntohl(high1)
            high2 = socket.ntohl(high2)
            low1 = socket.ntohl(low1)
            low2 = socket.ntohl(low2)
            #print(high1, high2, low1, low2)

            high = (high1 << 32) + high2
            low = (low1 << 32) + low2
            #print(high, low)

            return "-%u.%020u"%(high, low)


print(IpFormatTrans.ip_ntop("2887718680.00000000000000000000"))
print(IpFormatTrans.ip_ntop("-2306405959167115264.00000000000000000001"))

print(IpFormatTrans.ip_pton("172.30.164.42"))
print(IpFormatTrans.ip_pton("2002::1"))


