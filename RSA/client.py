import socket
from tkinter import *

import RSA.rsa as rsa

sock = socket.socket()
serverIP = ""
serverPort = 0
keygen = rsa.RSAKeyGen()
e, n = keygen.get_public_key()
d = keygen.get_secret_key()
flag = True


def initConnection(a: str, b: int):
    global serverIP, serverPort
    try:
        sock.connect((a, int(b)))
    except Exception as e:
        root.title("Can't connect!")
        print(e)
        return
    root.title("Connected")
    serverIP, serverPort = a, b
    frame.destroy()
    reg()


def connect_to_server():
    global frame
    frame.pack(padx=5, pady=5, expand=1)
    sub_frame = Frame(frame)
    sub_frame.grid(row=0, column=0, sticky="w")

    serverIP_label = Label(sub_frame, text="Server IP-address:")
    serverPort_label = Label(sub_frame, text="Server port:")

    serverIP_label.grid(row=0, column=0, sticky="w")
    serverPort_label.grid(row=1, column=0, sticky="w")

    serverIP_entry = Entry(sub_frame)
    serverPort_entry = Entry(sub_frame)

    serverIP_entry.grid(row=0, column=1, padx=5, pady=5)
    serverPort_entry.grid(row=1, column=1, padx=5, pady=5)
    connect_button = Button(frame, text="Connect!",
                            command=lambda: initConnection(serverIP_entry.get(), serverPort_entry.get()))
    connect_button.grid(row=1, column=0, padx=10, pady=10)


def sendUserName(name: str, notification: StringVar):
    global flag
    if flag:
        sock.send(b'\x11\x11')
        flag = False
    nameB = name.encode('utf-8')
    if len(nameB) > 40:
        notification.set("Too long name!")
        return
    sock.send(nameB)
    if sock.recv(2) == b'\x00\x00':
        notification.set('The name "' + name + '" already in use. Choose another one!')
        return
    sock.send(e.to_bytes(256, byteorder='big', signed=False))
    sock.send(n.to_bytes(256, byteorder='big', signed=False))
    frame.destroy()


def reg():
    global frame
    frame = LabelFrame(root, text='Registration')
    frame.pack(padx=5, pady=5, expand=1)
    message = StringVar()
    label = Label(frame, textvariable=message)
    message.set("Enter your name:")
    label.grid(row=0, column=0, padx=10, pady=10)
    username_entry = Entry(frame)
    username_entry.grid(row=1, column=0)
    btn = Button(frame, text="Send!", command=lambda: sendUserName(username_entry.get(), message))
    btn.grid(row=2, column=0)


root = Tk()
frame = LabelFrame(root, text="Enter server address")
root.geometry("400x600+400+50")
root.title("RSA-клиент. Автор: Саидмуродов Сирожиддин")
root.resizable(0, 0)
connect_to_server()
root.mainloop()
