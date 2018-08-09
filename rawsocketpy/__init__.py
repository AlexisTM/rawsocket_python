#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A Raw socket implementation allowing any ethernet type to be used/sniffed.

If gevent is available, sockets are monkey patched and two additionnal asynchronous server implementations are available: :class:`RawAsyncServer`, :class:`RawAsyncServerCallback` 

.. moduleauthor:: Alexis Paques <alexis.paques@gmail.com>
"""

from __future__ import print_function
try:
    from gevent import monkey; monkey.patch_all()
    from .asyncserver import RawAsyncServer, RawAsyncServerCallback
except ImportError:
    print("Gevent could not be loaded; the sockets will not be cooperative.")

from .util import get_hw, protocol_to_ethertype, to_bytes, to_str
from .socket import RawSocket
from .packet import RawPacket
from .server import RawServer, RawRequestHandler, RawServerCallback
