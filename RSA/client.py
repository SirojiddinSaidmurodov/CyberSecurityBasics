import socket
from tkinter import *

import RSA.rsa as rsa


class Client:
    def __init__(self, root_widget: Tk):
        self.sock = socket.socket()
        self.serverAdr = ('', 0)
        self.adr = ('', 0)
        self.peerAdr = ('', 0)
        self.peerKey = (0, 0)
        self.username = ""
        self.keygen = rsa.RSAKeyGen()
        self.pKey = self.keygen.get_public_key()
        self.sKey = self.keygen.get_secret_key()
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
                                command=lambda: self.__initConnection__(serverIP_entry.get(),
                                                                        int(serverPort_entry.get())))
        connect_button.grid(row=1, column=0, padx=10, pady=10)

    def __initConnection__(self, a: str, b: int):
        try:
            self.sock.connect((a, b))
        except Exception as e:
            self.root.title("Can't connect!")
            print(e)
            return
        self.root.title("Connected")
        self.serverAdr = (a, b)
        self.adr = self.sock.getsockname()
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
        e, n = self.pKey
        self.sock.send(e.to_bytes(256, byteorder='big', signed=False))
        self.sock.send(n.to_bytes(256, byteorder='big', signed=False))
        self.username = name
        self.frame.destroy()
        self.sock.close()
        self.__new_chat__()

    def __new_chat__(self):
        self.frame = LabelFrame(self.root, text="Creating new chat")
        self.frame.pack(padx=5, pady=5, expand=1)
        btn1 = Button(self.frame, text="Connect to peer", command=self.__connect_to_peer__())
        btn2 = Button(self.frame, text="Wait for connection", command=self.__wait__())
        btn1.grid(row=0, column=0, padx=10, pady=10)
        btn2.grid(row=1, column=0, padx=10, pady=10)

    def __wait__(self):
        self.frame.destroy()
        self.root.title("Waiting for connection")
        self.sock = socket.socket()
        self.sock.bind(self.adr)
        self.sock.listen(1)
        conn, self.peerAdr = self.sock.accept()
        #  TODO: waiting for connection

    def __connect_to_peer__(self):
        self.frame.destroy()
        self.frame = LabelFrame(self.root, text="Enter peer name")
        self.frame.pack(padx=5, pady=5, expand=1)
        entry = Entry(self.frame)
        entry.grid(row=0, column=0, padx=10, pady=10)
        btn = Button(self.frame, command=self.__get_user_while_connect__)
        btn.grid(row=0, column=1, padx=10, pady=10)

    def __get_user__(self):
        self.sock = socket.socket()
        self.sock.connect(self.serverAdr)
        self.sock.send(b'\x55\x55')
        if self.sock.recv(2) == b'\x00\x00':
            return False
        self.peerKey = (int.from_bytes(self.sock.recv(256), byteorder='big', signed=False),
                        int.from_bytes(self.sock.recv(256), byteorder='big', signed=False))
        self.peerAdr = (
            self.sock.recv(50).decode("utf-8"), int.from_bytes(self.sock.recv(16), byteorder='big', signed=False))
        self.sock.close()
        return True

    def __get_user_while_connect__(self):
        if not self.__get_user__():
            return
        else:
            self.__chat_create_


if __name__ == "__main__":
    root = Tk()
    client = Client(root)
    client.start()

    root.mainloop()
