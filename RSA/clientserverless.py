import random
import socket

from RSA.rsa import RSAKeyGen


class Client:
    def __init__(self):
        self.receiver = socket.socket
        self.sender = socket.socket
        self.keygen = RSAKeyGen()

    def host_mode(self):
        sock = socket.socket()
        sock.bind(('localhost', 9090))
        adr = sock.getsockname()
        print(adr)
        sock.listen(1)
        self.receiver, adr = sock.accept()
        peerIP = self.receiver.recv(50).decode("utf-8")
        peerPort = int.from_bytes(self.receiver.recv(50), byteorder='big', signed=False)
        self.sender = socket.socket()
        self.sender.connect((peerIP, peerPort))
        print("ok")

    def connect_mode(self, adr: tuple):
        sock = socket.socket()
        sock.bind(('localhost', random.randint(5000, 65000)))
        myAdr = sock.getsockname()
        ip, port = myAdr
        self.sender = socket.socket()
        self.sender.connect(adr)
        self.sender.send(ip.encode("utf-8"))
        self.sender.rec
        self.sender.send(port.to_bytes(50, byteorder='big', signed=False))
        self.receiver, _ = sock.accept()
        print("ok")
