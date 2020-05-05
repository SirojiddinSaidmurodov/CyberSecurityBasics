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
        self.length = (length // 4)
        self.cache = []

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

    def send(self, message: str):
        message_bytes = message.encode('utf-8')
        padding_length = (self.length - len(message_bytes) % self.length)
        if padding_length > 0:
            message_bytes = message_bytes + b'\x00' * padding_length
        chunks = [message_bytes[i: i + self.length - 1] for i in range(0, len(message_bytes), self.length - 1)]
        for chunk in chunks:
            hidden_message = rsa.encrypt((int.from_bytes(chunk, byteorder='big', signed=False)), self.peerKey)
            self.sender.send(hidden_message.to_bytes(self.length, byteorder='big', signed=False))
        self.sender.send(b'\x00\x00')

    def listen(self, root, chat):
        self.receiver.setblocking(False)
        try:
            chunk = self.receiver.recv(self.length)
            if chunk != b'\x00\x00':
                plain = self.keygen.decrypt(int.from_bytes(chunk, byteorder='big', signed=False))
                plain_bytes = int.to_bytes(plain, self.length - 1, byteorder='big', signed=False)
                self.cache.append(plain_bytes.rstrip(b'\x00'))
            else:
                message_bytes = b''.join(self.cache)
                print(message_bytes)
                message_text = message_bytes.decode('utf-8')
                print(message_text)
                text = "\n" + self.peerName + ":\n" + message_text + "\n"
                chat.insert(END, text)
                self.cache.clear()
        except Exception:
            root.after(1, lambda: self.listen(root, chat))
            return
        root.after(1, lambda: self.listen(root, chat))
        return
