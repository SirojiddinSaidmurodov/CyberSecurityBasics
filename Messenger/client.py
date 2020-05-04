import socket
from tkinter import *

import RSA.rsa as rsa


class Client:
    def __init__(self):
        self.sender = socket.socket()
        self.receiver = socket.socket()
        self.serverAdr = self.adr = self.peerAdr = ('', 0)
        self.username = self.peerName = ""
        self.peerKey = (0, 0)
        self.keygen = rsa.RSAKeyGen()
        self.pKey = self.keygen.get_public_key()

    def connect2server(self, name, address):
        sock = socket.socket()
        try:
            sock.connect(address)
        except Exception:
            raise Exception("Can't connect")
        sock.send(b'\x11\x11')
        self.serverAdr = address
        self.adr = sock.getsockname()
        sock.send(name.encode('utf-8'))
        if sock.recv(2) == b'\x00\x00':
            sock.close()
            raise Exception('The name "' + name + '" already in use. Choose another one!')
        e, n = self.pKey
        sock.send(e.to_bytes(256, byteorder='big', signed=False))
        sock.send(n.to_bytes(256, byteorder='big', signed=False))
        self.username = name
        sock.close()

    def get_peer(self, name: str):
        sock = socket.socket()
        sock.connect(self.serverAdr)
        sock.send(b'\x55\x55')
        sock.send(name.encode('utf-8'))
        if sock.recv(2) == b'\x11\x11':
            self.peerName = name
            self.peerKey = (int.from_bytes(sock.recv(256), byteorder='big', signed=False),
                            int.from_bytes(sock.recv(256), byteorder='big', signed=False))
            self.peerAdr = (
                sock.recv(50).decode("utf-8"), int.from_bytes(sock.recv(16), byteorder='big', signed=False))
            sock.close()
            return True
        sock.close()
        return False

    def wait(self):
        sock = socket.socket()
        sock.bind(self.adr)
        sock.listen(1)
        self.receiver, _ = sock.accept()
        self.peerName = self.receiver.recv(40).decode('utf-8')
        self.get_peer(self.peerName)
        self.sender = socket.socket()
        self.sender.connect(self.peerAdr)

    def connect2peer(self, name):
        if self.get_peer(name):
            self.sender = socket.socket()
            self.sender.connect(self.peerAdr)
            self.sender.send(self.username.encode("utf-8"))
            sock = socket.socket()
            sock.bind(self.adr)
            sock.listen(1)
            self.receiver, _ = sock.accept()
            return True
        else:
            return False

    def send(self, message):
        self.sender.send(message.encode('utf-8'))

    def listen(self, root, chat):
        self.receiver.setblocking(False)
        try:
            message = self.receiver.recv(1000).decode("utf-8")
            message = "\n" + self.peerName + ":\n" + message + "\n"
            chat.insert(END, message)
        except Exception:
            root.after(1, self.listen)
            return
        root.after(1, self.listen)
        return
