#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .packet import RawPacket
from .socket import RawSocket
from .util import get_hw, to_bytes, protocol_to_ethertype

class RawServer(object):
    """A **Blocking** base server implementation of a server on top of the RawSocket.
    It waits for data, encapsulate the data in the RequestHandlerClass provided and blocks until the RequestHandlerClass run() function finishes.  

    :note: packet = recv() 
           -> RequestHandlerClass(packet) 
           -> RequestHandlerClass.run()
           -> loop
    """
    def __init__(self, interface, protocol, RequestHandlerClass):
        """

        :param interface: interface to be used.
        :type interface: str
        :param protocol: Ethernet II protocol, RawSocket [1536-65535]
        :type protocol: int
        :param RequestHandlerClass: The class that will handle the requests
        :type RequestHandlerClass: RawServerCallback
        """
        self.RequestHandlerClass = RequestHandlerClass
        self.socket = RawSocket(interface, protocol)
        self.recv = self.socket.recv
        self.running = False

    def spin_once(self):
        """Handles the next message"""
        packet = self.recv()
        handler = self.RequestHandlerClass(packet, self)
        self.handle_handler(handler)

    def handle_handler(self, handler):
        """Manage the handler, can be overwritten"""
        handler.run()

    def spin(self):
        """Loops until self.running becomes False (from a Request Handler or another thread/coroutine)"""
        self.running = True
        while self.running:
            self.spin_once()


class RawServerCallback(RawServer):
    """A blocking server implementation that uses a centralized callback. This is useful for a stateful server.

    :note: packet = recv() 
           -> RequestHandlerClass(packet, self) 
           -> callback(RequestHandlerClass, self)
           -> loop
    """
    def __init__(self, interface, protocol, RequestHandlerClass, callback):
        """
        :param interface: interface to be used.
        :type interface: str
        :param protocol: Ethernet II protocol, RawSocket [1536-65535]
        :type protocol: int
        :param RequestHandlerClass: The class that will handle the requests
        :type RequestHandlerClass: RawServerCallback
        :param callback: callback to be used.
        :type callback: function
        """
        self.callback = callback
        RawServer.__init__(self, interface, protocol, RequestHandlerClass)
    
    def handle_handler(self, handler):
        """
        Overwritten: Calls callback(handler, self) instead.
        """
        self.callback(handler, self)


class RawRequestHandler(object):
    """The class that handles the request. 
    It has access to the packet and the server data.
    """
    def __init__(self, packet, server):
        self.packet = packet
        """:description: Packet received
        :type: RawPacket"""
        self.server = server
        """:description: Server from which the packet comes
        :type: RawServer"""

    def finish(self):
        """empty: To be **overwritten**"""
        pass
    
    def setup(self):
        """empty: To be **overwritten**"""
        pass

    def handle(self):
        """empty: To be **overwritten**"""
        pass
    
    def run(self):
        """Run the request handling process: 

        try:
            * self.setup()
            * self.handle()
        finally:
            * self.finish()
        """
        try:
            self.setup()
            self.handle()
        except Exception as e:
            print(e)
        finally:
            self.finish()
