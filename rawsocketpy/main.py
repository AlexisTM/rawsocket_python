#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, select, struct, time
from .util import get_hw, to_str, protocol_to_ethertype, to_bytes

class RawPacket():
    """RawPacket is the resulting data container of the RawSocket class. 

    It reads raw data and stores the MAC source, MAC destination, the Ethernet type and the data payload.

    RawPacket.success is true if the packet is successfuly read.
    """
    def __init__(self, data):
        """A really simple class.

        Args:
           foo (data): raw ethernet frame coming from the socket library, either **bytes in Python3** or **str in Python2**
        """
        self.dest = ""
        """(str/bytes/bytearray): destination
        """
        self.src = ""
        """(str/bytes/bytearray): source
        """
        self.type = ""
        """(str/bytes/bytearray): ethertype
        """
        self.data = ""
        """ = (str/bytes/bytearray): payload received, aka the msg sent on the other side
        """
        self.success = False
        try:
            self.dest, self.src, self.type = data[0:6], data[6:12], data[12:14]
            self.data = data[14:]
            self.success = True
        except Exception as e:
            print("rawsocket: ", e)
            self.success = False

    def __repr__(self):
        return "".join([to_str(self.src), " == 0x", to_str(self.type, separator=""), " => ", to_str(self.dest), " - ", "OK" if self.success else "FAILED"])

    def __str__(self):
        return "".join([self.__repr__(), ":\n", self.data.decode('utf-8')])

class RawSocket(object):
    """RawSocket is using the socket library to send raw ethernet frames, using socket.RAW_SOCK

    It has a similar API to the socket library: send/recv/close/dup.

    Args:
       interface (str): the network interface to be used: wlp2s0, eth0, zt0, wlan0, ...
       
       protocol (int): the ethertype to use: 0xEEAF for example [0 to 65535]
       
       sock (socket.socket): If provided, this socket will be used for the communications
       
       no_recv_protocol (bool): If True, the socket will not receive any data, for "sending only" sockets.
    """
    BROADCAST = "\xff\xff\xff\xff\xff\xff"
    def __init__(self, interface, protocol, sock=None, no_recv_protocol=False):
        if  not 0x0000 < protocol < 0xFFFF:
            raise ValueError("Protocol has to be in the range 0 to 65535")
        self.no_recv_protocol = no_recv_protocol
        self.non_processed_protocol = protocol
        self.protocol = socket.htons(protocol)
        self.ethertype = protocol_to_ethertype(protocol)
        self.interface = interface
        self.mac = get_hw(self.interface)
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

        Args:
           msg (str): Payload to be sent 
           
           dest (str/bytes/bytearray): recipient, if not mentioned it will be a broadcast example: "\xff\x12\x32\x34\x41" or bytes([255, 12, 32, 42, 43, 54])
           
           ethertype (str/bytes/bytearray): Allow to send data using a different ethertype using the same socket. Default is the protocol given in the constructor.
        """
        if ethertype is None: ethertype = self.ethertype
        if dest is None: dest = self.BROADCAST
        payload = (to_bytes(dest) + self.mac + to_bytes(ethertype) +  to_bytes(msg))
        self.sock.send(payload)

    def recv(self):
        """Receive data from the socket on the protocol provided in the constructor

        Blocks until data arrives. A timeout can be implemented using the socket timeout.

        Returns RawPacket
        """
        data = self.sock.recv(1500)
        return RawPacket(data)
    
    def __str__(self):
        return self.interface
