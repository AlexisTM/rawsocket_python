import socket, select, struct, time
from .util import get_hw, to_str, protocol_to_ethertype, to_bytes

class RawPacket():
    def __init__(self, data):
        self.dest = ""
        self.src = ""
        self.type = ""
        self.data = ""
        self.success = False
        try:
            self.dest, self.src, self.type = data[0:6], data[6:12], data[12:14]
            self.data = data[14:]
            self.success = True
        except Exception as e:
            print("rawsocket: ", e)
            self.success = False

    def __repr__(self):
        return "".join([to_str(self.src), " == 0x", to_str(self.type, separator=""), " => ", to_str(self.dest), " - ", "OK" if self.success else "FAILED"])

    def __str__(self):
        return "".join([self.__repr__(), ":\n", self.data.decode('utf-8')])

class RawSocket(object):
    BROADCAST = "\xff\xff\xff\xff\xff\xff"
    def __init__(self, interface, protocol, sock=None, no_recv_protocol=False):
        if  not 0x0000 < protocol < 0xFFFF:
            raise ValueError("Protocol has to be in the range 0 to 65535")
        self.no_recv_protocol = no_recv_protocol
        self.non_processed_protocol = protocol
        self.protocol = socket.htons(protocol)
        self.ethertype = protocol_to_ethertype(protocol)
        self.interface = interface
        self.mac = get_hw(self.interface)
        if no_recv_protocol:
            self.sock = self.sock_create(self.interface, 0, sock)
        else: 
            self.sock = self.sock_create(self.interface, self.protocol, sock)
        self.close = self.sock.close

    def dup(self):
        return RawSocket(self.interface, self.non_processed_protocol, self.sock.dup(), self.no_recv_protocol)

    @staticmethod
    def sock_create(interface, protocol, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, protocol)
            sock.bind((interface, 0))
        return sock

    def send(self, msg, dest=None, ethertype=None):
        if ethertype is None: ethertype = self.ethertype
        if dest is None: dest = self.BROADCAST
        payload = (to_bytes(dest) + self.mac + to_bytes(ethertype) +  to_bytes(msg))
        self.sock.send(payload)

    def recv(self):
        data = self.sock.recv(1500)
        return RawPacket(data)
    
    def __str__(self):
        return self.interface
