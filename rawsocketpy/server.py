#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .main import RawPacket, RawSocket
from .util import get_hw, to_bytes, protocol_to_ethertype

class RawServer(object):
    def __init__(self, interface, protocol, RequestHandlerClass):
        self.RequestHandlerClass = RequestHandlerClass
        self.socket = RawSocket(interface, protocol)
        self.recv = self.socket.recv
        self.running = False

    def spin_once(self):
        packet = self.recv()
        handler = self.RequestHandlerClass(packet, self)
        self.handle_handler(handler)

    def handle_handler(self, handler):
        handler.run()

    def spin(self):
        self.running = True
        while self.running:
            self.spin_once()


class RawServerCallback(RawServer):
    def __init__(self, interface, protocol, RequestHandlerClass, callback):
        self.callback = callback
        RawServer.__init__(self, interface, protocol, RequestHandlerClass)
    
    def handle_handler(self, handler):
        self.callback(handler, self)


class RawRequestHandler(object):
    def __init__(self, packet, server):
        self.packet = packet
        self.server = server
        # self.server.socket.sock = low level socket

    def finish(self):
        pass
    
    def setup(self):
        pass

    def handle(self):
        print(self.packet)
    
    def run(self):
        try:
            self.setup()
            self.handle()
        except Exception as e:
            print(e)
        finally:
            self.finish()
