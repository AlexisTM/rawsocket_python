#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .server import RawServer, RawServerCallback
from gevent import pool, Greenlet

class RawAsyncServer(RawServer):
    pool = pool.Pool()
    def handle_handler(self, handler):
        self.pool.start(Greenlet(handler.run))

class RawAsyncServerCallback(RawServerCallback, RawAsyncServer):
    def handle_handler(self, handler):
        self.pool.start(Greenlet(self.callback, handler, self))
