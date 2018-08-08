# RawSocketPy

Raw socket is a layer 2 python library for communication using the MAC addresses only. 

This allows you to create a custom made Ethernet/WiFi communication system which is **not** using IP nor TCP/UDP or to debug custom frames such as SERCOS III, Profibus, ARP, PTP, ...

Python versions tested:

- [x] 2.7.x
- [x] 3.5.x

OSes:

- [ ] Linux 14.04
- [x] Linux 16.04
- [ ] Linux 18.04
- [ ] Windows 10
- [ ] Mac OSX

**Pros:**

- Low level
- Not using TCP-UDP/IP
- Dead simple
- Can broadcast
- MTU of 1500

**Cons:**

- Low level
- Not using TCP-UDP/IP
- No encryption
- No fragmentation
- **Requires root**
- MTU of 1500

## Installation

```bash
# Soon
sudo -H pip install rawsocketpy

# for now:
git clone https://github.com/AlexisTM/rawsocket_python
cd rawsocket_python
sudo python setup.py install
```

## Fast testing

On one computer:

```bash
sudo python -c "from rawsocketpy import RawSocket
sock = RawSocket('wlp2s0', 0xEEFA)
while True: print(sock.recv())"

# 12:34:56:78:9A:BC == 0xEEFA => FF:FF:FF:FF:FF:FF - OK:
# Boo
```

On the second computer:

```bash
sudo python -c "from rawsocketpy import RawSocket
sock = RawSocket('wlp2s0', 0xEEFA)
>hile True: print(sock.send('Boo'))"
```

## In-depth

```python
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
```

### Receiving

On another machine, you can run the following:

```python
from rawsocketpy import RawSocket, u_to_str

sock = RawSocket("wlp2s0", 0xEEFA)
packet = sock.recv()
# The type of packet is RawPacket() which allows pretty printing and unmarshal the raw data.

print(packet) # Pretty print
packet.dest   # unicode string "\xFF\xFF\xFF\xFF\xFF\xFF"
packet.src    # unicode string "\x12\x12\x12\x12\x12\x13"
packet.type   # unicode string "\xEE\xFA"
packegt.data  # unicode string "some data"

print u_to_str(packet.dest)     # Human readable MAC:  FF:FF:FF:FF:FF:FF
print u_to_str(packet.type, "") # Human readable type: EEFA
```

## I want to contribue!!

You are free to contribue, the following capabilities are welcome:

- Windows compatibility
- Async implementation (callbacks on new data)
- Readthedocs documentation
- More Python versions and OS tests

## Credits

- Alexis PAQUES - [@AlexisTM](https://github.com/AlexisTM/)
