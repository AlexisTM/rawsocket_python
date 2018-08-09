Asynchronous Server with custom data handler
===============================================

To a raw server, you have the following options:

* RawServer: Blocks for each message received until handled
* RawServerCallback: Calls the callback and blocks until the callback returns
* RawServerAsync: **if gevent available**, it will handle the incomming messages in a pool of Greenlets
* RawServerAsyncCallback: **if gevent available**, it will add the callback in a pool of Greenlets

.. code-block:: python
   :caption: First machine
   :name: First machine
    
   from rawsocketpy import RawRequestHandler, RawAsyncServerCallback
   import time


   def some_callback(handler, server):
       print("callback")
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
       rs = RawAsyncServerCallback("wlp2s0", 0xEEFA, LongTaskTest, some_callback)
       rs.spin()
   if __name__ == '__main__':
       main()

