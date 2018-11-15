#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import socket, select, struct, time
from .packet import RawPacket
from .util import get_hw, to_str, protocol_to_ethertype, to_bytes

class RawSocket(object):
    """RawSocket is using the socket library to send raw ethernet frames, using socket.RAW_SOCK

    It has a similar API to the socket library: send/recv/close/dup.
    """
    BROADCAST = "\xff\xff\xff\xff\xff\xff"
    """:description: Default MAC address: ``"\\xff\\xff\\xff\\xff\\xff\\xff"``"""
    def __init__(self, interface, protocol, sock=None, no_recv_protocol=False):
        """

        :param interface: interface to be used.
        :type interface: str
        :param protocol: Ethernet II protocol, RawSocket [1536-65535]
        :type protocol: int
        :param socket: Socket to be used (default None), if not given, a new one will be created.
        :type socket: socket.socket
        :param no_recv_protocol: If true (default False), the socket will not subscribe to anything, recv will just block.
        :type no_recv_protocol: bool
        """
        if  not protocol < 0xFFFF:
            raise ValueError("Protocol has to be in the range 0 to 65535")
        self.no_recv_protocol = no_recv_protocol
        self.non_processed_protocol = protocol
        self.protocol = socket.htons(protocol)
        self.ethertype = protocol_to_ethertype(protocol)
        self.interface = interface
        self.mac = get_hw(self.interface)
        """:description: Source MAC address used for communications - could be modified after initialization
        :type: str/bytes/bytearray"""
        if no_recv_protocol:
            self.sock = self.sock_create(self.interface, 0, sock)
        else:
            self.sock = self.sock_create(self.interface, self.protocol, sock)
        self.close = self.sock.close

    def dup(self):
        """Duplicates the RawSocket
        """
        return RawSocket(self.interface, self.non_processed_protocol, self.sock.dup(), self.no_recv_protocol)

    @staticmethod
    def sock_create(interface, protocol, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, protocol)
            sock.bind((interface, 0))
        return sock

    def send(self, msg, dest=None, ethertype=None):
        """Sends data through the socket.

        :param msg: Payload to be sent
        :type msg: str/bytes/bytearray
        :param dest: recipient such as ``"\\xff\\x12\\x32\\x34\\x41"`` or ``bytes([1,2,3,4,5,6])``. It will broadcast if no given default(None)
        :type dest: str/bytes/bytearray
        :param ethertype: Allow to send data using a different ethertype using the same socket. Default is the protocol given in the constructor.
        :type ethertype: str/bytes/bytearray
        """
        if ethertype is None: ethertype = self.ethertype
        if dest is None: dest = self.BROADCAST
        payload = dest + self.mac + ethertype + msg
        self.sock.send(payload)

    def recv(self):
        """Receive data from the socket on the protocol provided in the constructor

        Blocks until data arrives. A timeout can be implemented using the socket timeout.

        :rtype: RawPacket
        """
        data = self.sock.recv(1024)
        return RawPacket(data)
    
    def __str__(self):
        return self.interface
