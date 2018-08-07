import socket, select, struct, time
from get_hw import get_hw, u_to_str

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
        except:
            self.success = False

    def __repr__(self):
        return "".join([u_to_str(self.src), " == 0x", u_to_str(self.type, separator=""), " => ", u_to_str(self.dest), " - ", "OK" if self.success else "FAILED"])

    def __str__(self):
        return "".join([self.__repr__(), ":\n", self.data])

class RawSocket(object):
    BROADCAST = "\xff\xff\xff\xff\xff\xff"
    def __init__(self, interface, protocol, sock=None, no_recv_protocol=False):
        if  not 0x0000 < protocol < 0xFFFF:
            raise ValueError("Protocol has to be in the range 0 to 65535")
        self.protocol = socket.htons(protocol)
        self.ethertype = self.protocol_to_ethertype(protocol)
        self.interface = interface
        self.mac = get_hw(self.interface)
        if no_recv_protocol:
            self.sock = self.sock_create(self.interface, 0, sock)
        else: 
            self.sock = self.sock_create(self.interface, self.protocol, sock)

    @staticmethod
    def sock_create(interface, protocol, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, protocol)
            sock.bind((interface, 0))
        return sock

    @staticmethod
    def protocol_to_ethertype(protocol):
        return chr((protocol & 0xFF00) >> 8) + chr(protocol & 0x00FF)

    def send(self, msg, dest=None, ethertype=None):
        if ethertype is None: ethertype = self.ethertype
        if dest is None: dest = self.BROADCAST
        self.sock.send(dest + self.mac + ethertype + msg)

    def recv(self):
        data = self.sock.recv(1500)
        return RawPacket(data)
    
    def __str__(self):
        return self.interface

def main():
    na = NetworkAdapter("wlp2s0", 0xAA42)
    i = 0
    while True:
        try:
            na.send(str(i))
            time.sleep(0.1)
            i += 1
        except:
            break

if __name__ == '__main__':
    main()