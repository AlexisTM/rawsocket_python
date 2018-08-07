#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import fcntl
import struct
import sys

if sys.version_info >= (3,0):
    import binascii
    def get_hw(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s',  bytes(ifname[:15], 'utf-8')))
        return info[18:24]

    def u_to_str(data, separator=":"):
        return separator.join("{:02x}".format(ord(c)) for c in data).upper()
else:

    def get_hw(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        return info[18:24]

    def u_to_str(data, separator=":"):
        return separator.join("{:02x}".format(ord(c)) for c in data).upper()

def main():
    print u_to_str(get_hw("wlp2s0"))

if __name__ == '__main__':
    main()
