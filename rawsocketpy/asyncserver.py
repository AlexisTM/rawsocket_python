#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from .server import RawServer, RawServerCallback
from gevent import pool, Greenlet

class RawAsyncServer(RawServer):
    """
    Prefered server instead of RawServer.
    Async server using :class:`gevent.Greenlet` in a :class:`gevent.pool` to allow asynchronous calls.

    This will ensure you are not loosing data because the handler is too long.
    """
    pool = pool.Pool()
    def handle_handler(self, handler):
        """Add the Greenlet to the pool with ``handler.run()``, the function to run.
        
        :param handler: The RawRequestHandler provided in the constructor
        :type handler: RawRequestHandler"""
        self.pool.start(Greenlet(handler.run))

class RawAsyncServerCallback(RawServerCallback, RawAsyncServer):
    """
    Async server using :class:`gevent.Greenlet` in a :class:`gevent.pool` to allow asynchronous calls.
    """
    def handle_handler(self, handler):
        """Add the Greenlet to the pool with ``self.callback(handler, self)``: the function to run.
        
        :param handler: The RawRequestHandler provided in the constructor
        :type handler: RawRequestHandler"""
        self.pool.start(Greenlet(self.callback, handler, self))
