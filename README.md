# RawSocketPy

Raw socket is a layer 2 python library for communication using the MAC addresses only. 

This allows you to create a custom made Ethernet/WiFi communication system which is **not** using IP nor TCP/UDP or to debug custom frames such as SERCOS III, Profibus, ARP, PTP, ...

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

## Usage

### Sending

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

# On capable hardware, you can spoof your MAC address:
sock.mac = "\x12\x13\x14\x15\x16\x17"
sock.send("some data")
```

### Receiving

On another machine, you can run the following:

```python
from rawsocketpy import RawSocket, u_to_str

sock = RawSocket("wlp2s0", 0xEEFA)
packet = sock.recv()

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
- Python 3.x compatibility
- Server implementation (callbacks on new data)

## Credits

- Alexis PAQUES - [@AlexisTM](https://github.com/AlexisTM/)