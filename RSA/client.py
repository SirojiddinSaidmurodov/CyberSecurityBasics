import socket

import RSA.rsa as rsa
from tkinter import *

sock = socket.socket()


def reg(a: str, b):
    try:
        sock.connect((a, int(b)))
    except Exception as e:
        root.title("Can't connect!")
        print(e)
        return
    root.title("Connected")
    frame.destroy()


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
    connect_button = Button(frame, text="Connect!", command=lambda: reg(serverIP_entry.get(),serverPort_entry.get()))
    connect_button.grid(row=1, column=0, padx=10, pady=10)


root = Tk()
frame = LabelFrame(root, text="Enter server address")
root.geometry("400x600+400+50")
root.title("RSA-клиент. Автор: Саидмуродов Сирожиддин")
root.resizable(0, 0)
connect_to_server()

root.mainloop()
