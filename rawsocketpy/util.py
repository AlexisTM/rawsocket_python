#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import socket
import fcntl
import struct
import sys

if sys.version_info >= (3, 0):
    import binascii

    def get_hw(ifname):
        """Returns a bytearray containing the MAC address of the interface.

        :param ifname: Interface name such as ``wlp2s0``
        :type ifname: str
        :rtype: str
        :rtype: bytearray
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(
            '256s',  bytearray(ifname[:15], 'utf-8')))
        return info[18:24]
else:
    def get_hw(ifname):
        """Returns a unicode string containing the MAC address of the interface.

        :param ifname: Interface name such as ``wlp2s0``
        :type ifname: str
        :rtype: str
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,
                           struct.pack('256s', ifname[:15]))
        return info[18:24]


def to_str(data, separator=":"):
    """Stringify hexadecimal input;

    :param data: Raw data to print
    :type data: str or bytes or bytearray
    :param separator: The separator to be used **between** the two digits hexadecimal data.
    :type separator: str

    >>> to_str(bytes([1,16,5]))
    "01:0F:05"
    >>> to_str(bytes([1,16,5]), separator="")
    "010F05"
    """
    if type(data) is str:
        return separator.join(["{:02x}".format(ord(c)) for c in data])
    if type(data) in [bytes, bytearray]:
        return separator.join(["{:02x}".format(c) for c in data])
    else:
        return str(data)


def protocol_to_ethertype(protocol):
    """Convert the int protocol to a two byte chr.

    :param protocol: The protocol to be used such as 0x8015
    :type protocol: int
    :rtype: str
    """
    return chr((protocol & 0xFF00) >> 8) + chr(protocol & 0x00FF)


if sys.version_info >= (3, 0):
  def to_bytes(*data):
      """Flatten the arrays and Converts data to a bytearray

      :param data: The data to be converted
      :type data: [int, bytes, bytearray, str, [int], [bytes], [bytearray], [str]]
      :rtype: bytearray

      >>> to_bytes("123")
      b'123'
      >>> to_bytes(1, 2, 3)
      b'\\x01\\x02\\x03'
      >>> to_bytes("\\xff", "\\x01\\x02")
      b'\\xff\\x01\\x02'
      >>> to_bytes(1, 2, 3, [4,5,6])
      b'\\x01\\x02\\x03\\x04\\x05\\x06'
      >>> to_bytes(bytes([1,3,4]), bytearray([6,7,8]), "\\xff")
      b'\\x01\\x03\\x04\\x06\\x07\\x08\\xff'
      """
      result = bytearray()
      for d in data:
          if type(d) in [tuple, list]:
              baa = map(to_bytes, d)
              for ba in baa:
                  result += ba
          if type(d) is int:
              result += bytearray([d])
          if type(d) is str:
              result += bytearray(map(ord, d))
          if type(d) in [bytes, bytearray]:
              result += d
      return result
else:
  def to_bytes(*data):
      return bytes("".join(map(str, data)))
