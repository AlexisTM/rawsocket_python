Make it a server
================

Stateless blocking server example: Each time you receive a packet, it will be of type ``LongTaskTest`` and run ``setup()``, ``handle()`` and finally ``finish``. 
If the handle/setup fails, the ``finish`` function will be executed.

.. code-block:: python
    :caption: Blocking Stateless
    :name: Blocking Stateless

    from rawsocketpy import RawServer, RawRequestHandler

    class LongTaskTest(RawRequestHandler):
        def setup(self):
            print("Begin") 

        def handle(self):
            time.sleep(1)
            print(self.packet)

        def finish(self):
            print("End")

    def main():
        rs = RawServer("wlp2s0", 0xEEFA, LongTaskTest)
        rs.spin()

    if __name__ == '__main__':
        main()

**Statefull** and **blocking** server using a centralised callback. It does guarantee that the callback is called in ethernet packet order, but if the execution is long, you will loose packets.

.. code-block:: python
    :caption: Blocking Statefull
    :name: Blocking Statefull

    from rawsocketpy import RawServerCallback, RawRequestHandler

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
        rs = RawServerCallback("wlp2s0", 0xEEFA, LongTaskTest, callback)
        rs.spin()

    if __name__ == '__main__':
        main()
