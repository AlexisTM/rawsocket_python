Quicktest
=======================================

The simplest example to ensure the library is working for you is to take two machines (or one with two network cards) and run the following.

> Ensure to set **your interface** name instead of **wlp2s0**.

On the first machine:

.. code-block:: bash
   :caption: First machine
   :name: First machine

   sudo python -c "from rawsocketpy import RawSocket
   sock = RawSocket('wlp2s0', 0xEEFA)
   while True: print(sock.recv())"

On the second machine:

.. code-block:: bash
   :caption: Second machine
   :name: Second machine

    sudo python -c "from rawsocketpy import RawSocket; import time
    sock = RawSocket('wlp2s0', 0xEEFA)
    while True:
      sock.send('Boo')
      print('Boo has been sent')
      time.sleep(0.5)"

