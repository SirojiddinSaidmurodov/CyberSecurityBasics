import socket
from tkinter import *

import RSA.rsa as rsa


class Client:
    def __init__(self, length=512):
        self.sender = socket.socket()
        self.receiver = socket.socket()
        self.serverAdr = self.adr = self.peerAdr = ('', 0)
        self.userName = self.peerName = ""
        self.peerKey = (0, 0)
        self.keygen = rsa.RSAKeyGen(length)
        self.pKey = self.keygen.get_public_key()
        self.keygen.get_secret_key()
        self.length = self.keygen.get_length()

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
        self.userName = name
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
            self.sender.send(self.userName.encode("utf-8"))
            sock = socket.socket()
            sock.bind(self.adr)
            sock.listen(1)
            self.receiver, _ = sock.accept()
            return True
        else:
            return False

    def send(self, message):
        length = self.length // 2
        chunks = [message[i: i + length] for i in range(0, len(message), length)]
        for chunk in chunks:
            chunk_bytes: bytes = chunk.encode('utf-8')
            hidden_message = rsa.encrypt(int.from_bytes(chunk_bytes, byteorder='big', signed=False), self.peerKey)
            self.sender.send(hidden_message.to_bytes(self.length + 1, byteorder='big', signed=False))

    def listen(self, root, chat):
        self.receiver.setblocking(False)
        try:
            message = self.receiver.recv(self.length + 1)
            plain_message = int.to_bytes(self.keygen.decrypt(int.from_bytes(message, byteorder='big', signed=False)),
                                         self.length, byteorder='big', signed=False)
            print(plain_message.decode('utf-8'))
            text = "\n" + self.peerName + ":\n" + plain_message.decode('utf-8') + "\n"
            chat.insert(END, text)
        except Exception:
            root.after(1, lambda: self.listen(root, chat))
            return
        root.after(1, lambda: self.listen(root, chat))
        return
