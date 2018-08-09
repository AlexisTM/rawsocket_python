Low level socket
================

You can use the library with a low level socket, where you handle to send and receive.

.. code-block:: python
    :caption: Sending data
    :name: Sending data

    from rawsocketpy import RawSocket

    # 0xEEFA is the ethertype
    # The most common are available here: https://en.wikipedia.org/wiki/EtherType
    # The full official list is available here: https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries 
    # Direct link: https://standards.ieee.org/develop/regauth/ethertype/eth.csv
    # You can use whatever you want but using a already use type can have unexpected behaviour.
    sock = RawSocket("wlp2s0", 0xEEFA)

    sock.send("some data") # Broadcast "some data" with an ethertype of 0xEEFA

    sock.send("personal data", dest="\xAA\xBB\xCC\xDD\xEE\xFF") # Send "personal data to \xAA\xBB\xCC\xDD\xEE\xFF with an ether type of 0xEEFA

    sock.send("other data", ethertype="\xEE\xFF") # Broadcast "other data" with an ether type of 0xEEFF


.. code-block:: python
    :caption: Receiving data
    :name: Receiving data

    from rawsocketpy import RawSocket, to_str

    sock = RawSocket("wlp2s0", 0xEEFA)
    packet = sock.recv()
    # The type of packet is RawPacket() which allows pretty printing and unmarshal the raw data.

    # If you are using Python2, all data is encoded as unicode strings "\x01.." while Python3 uses bytearray.

    print(packet) # Pretty print
    packet.dest   # string "\xFF\xFF\xFF\xFF\xFF\xFF" or bytearray(b"\xFF\xFF\xFF\xFF\xFF\xFF")
    packet.src    # string "\x12\x12\x12\x12\x12\x13" or bytearray(b"\x12\x12\x12\x12\x12\x13")
    packet.type   # string "\xEE\xFA" or bytearray([b"\xEE\xFA"]
    packegt.data  # string "some data" or bytearray(b"some data"]

    print(to_str(packet.dest))     # Human readable MAC:  FF:FF:FF:FF:FF:FF
    print(to_str(packet.type, "")) # Human readable type: EEFA
