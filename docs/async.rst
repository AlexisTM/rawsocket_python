Go asynchronous
===============================================

Install gevent and you are ready to use asynchronous servers. The asynchronous server is a very small modification from the base :class:`RawServer`.

.. code-block:: bash
   :caption: Gevent installation command
   :name: Gevent installation command
    
   sudo pip -H install gevent


**Stateless** **Asynchronous** server:

.. code-block:: python
   :caption: Stateless Asynchronous server
   :name: Stateless Asynchronous server
    
   from rawsocketpy import RawRequestHandler, RawAsyncServer
   import time

   class LongTaskTest(RawRequestHandler):
       def handle(self):
           time.sleep(1)
           print(self.packet)

       def finish(self):
           print("End")

       def setup(self):
           print("Begin") 

   def main():
       rs = RawAsyncServer("wlp2s0", 0xEEFA, LongTaskTest)
       rs.spin()

   if __name__ == '__main__':
       main()

**Statefull** **Asynchronous** server:

.. code-block:: python
   :caption: Statefull Asynchronous server
   :name: Statefull Asynchronous server
        
    from rawsocketpy import RawRequestHandler, RawAsyncServerCallback
    import time

    def callback(handler, server):
        print("Testing")
        handler.setup()
        handler.handle()
        handler.finish()

    class LongTaskTest(RawRequestHandler):
        def handle(self):
            time.sleep(1)
            print(self.packet)

        def finish(self):
            print("End")

        def setup(self):
            print("Begin") 

    def main():
        rs = RawAsyncServerCallback("wlp2s0", 0xEEFA, LongTaskTest, callback)
        rs.spin()

    if __name__ == '__main__':
        main()

