#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .util import to_str, to_bytes

class RawPacket():
    """RawPacket is the resulting data container of the RawSocket class. 

    It reads raw data and stores the MAC source, MAC destination, the Ethernet type and the data payload.

    RawPacket.success is true if the packet is successfuly read.
    """
    def __init__(self, data):
        """A really simple class.

        :param data: raw ethernet II frame coming from the socket library, either **bytes in Python3** or **str in Python2**
        :type data: str or bytes or bytearray
        """
        self.dest = ""
        """:description: Destination MAC address
        :type: str or bytes or bytearray"""
        self.src = ""
        """:description: Source MAC address
        :type: str or bytes or bytearray"""
        self.type = ""
        """:description: Ethertype
        :type: str or bytes or bytearray"""
        self.data = ""
        """:description: Payload received
        :type: str or bytes or bytearray"""
        self.success = False
        """:description: True if the packet has been successfully unmarshalled 
        :type: bool"""
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
