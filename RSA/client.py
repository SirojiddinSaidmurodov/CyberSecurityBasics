import socket
from tkinter import *

import RSA.rsa as rsa


class Client:
    def __init__(self, root_widget: Tk):
        self.sock = socket.socket()
        self.serverIP, self.serverPort = '', 0
        self.IP, self.Port = '', 0
        self.peerIP, self.peerPort = '', 0
        self.keygen = rsa.RSAKeyGen()
        self.e, self.n = self.keygen.get_public_key()
        self.d = self.keygen.get_secret_key()
        self.root = root_widget
        self.frame = LabelFrame(root_widget, text="Enter server address")
        root_widget.geometry("400x600+400+50")
        root_widget.title("RSA-клиент. Автор: Саидмуродов Сирожиддин")
        root_widget.resizable(0, 0)

    def start(self):
        self.frame.pack(padx=5, pady=5, expand=1)
        sub_frame = Frame(self.frame)
        sub_frame.grid(row=0, column=0, sticky="w")

        serverIP_label = Label(sub_frame, text="Server IP-address:")
        serverPort_label = Label(sub_frame, text="Server port:")

        serverIP_label.grid(row=0, column=0, sticky="w")
        serverPort_label.grid(row=1, column=0, sticky="w")

        serverIP_entry = Entry(sub_frame)
        serverPort_entry = Entry(sub_frame)

        serverIP_entry.grid(row=0, column=1, padx=5, pady=5)
        serverPort_entry.grid(row=1, column=1, padx=5, pady=5)
        connect_button = Button(self.frame, text="Connect!",
                                command=lambda: self.__initConnection__(serverIP_entry.get(), serverPort_entry.get()))
        connect_button.grid(row=1, column=0, padx=10, pady=10)

    def __initConnection__(self, a: str, b: int):
        try:
            self.sock.connect((a, int(b)))
        except Exception as e:
            self.root.title("Can't connect!")
            print(e)
            return
        self.root.title("Connected")
        self.serverIP, self.serverPort = a, b
        self.IP, self.Port = self.sock.getsockname()
        self.frame.destroy()
        self.__reg__()

    def __reg__(self):
        self.frame = LabelFrame(self.root, text='Registration')
        self.frame.pack(padx=5, pady=5, expand=1)
        message = StringVar()
        label = Label(self.frame, textvariable=message)
        message.set("Enter your name:")
        label.grid(row=0, column=0, padx=10, pady=10)
        username_entry = Entry(self.frame)
        self.sock.send(b'\x11\x11')
        username_entry.grid(row=1, column=0)
        btn = Button(self.frame, text="Send!", command=lambda: self.__sendUserName__(username_entry.get(), message))
        btn.grid(row=2, column=0)

    def __sendUserName__(self, name: str, notification: StringVar):
        nameB = name.encode('utf-8')
        if len(nameB) > 40:
            notification.set("Too long name!")
            return
        self.sock.send(nameB)
        if self.sock.recv(2) == b'\x11\x11':
            notification.set('The name "' + name + '" already in use. Choose another one!')
            return
        self.sock.send(self.e.to_bytes(256, byteorder='big', signed=False))
        self.sock.send(self.n.to_bytes(256, byteorder='big', signed=False))
        self.frame.destroy()
        self.sock.close()
        self.__new_chat__()

    def __new_chat__(self):
        self.frame = LabelFrame(self.root, text="Creating new chat")
        self.frame.pack(padx=5, pady=5, expand=1)
        btn1 = Button(self.frame, text="Connect to peer")
        btn2 = Button(self.frame, text="Wait for connection")
        btn1.grid(row=0, column=0, padx=10, pady=10)
        btn2.grid(row=1, column=0, padx=10, pady=10)
        self.sock = socket.socket()
        self.sock.bind((self.IP, self.Port))


if __name__ == "__main__":
    root = Tk()
    client = Client(root)
    client.start()

    root.mainloop()
