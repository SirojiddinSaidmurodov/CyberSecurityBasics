from tkinter import *

import Messenger.client as client


class Messenger:
    def __init__(self, root):

        self.root = root
        self.root.geometry("400x600+400+50")
        self.root.title("RSA-клиент. Автор: Саидмуродов Сирожиддин")
        self.root.resizable(0, 0)
        self.chat: Text
        self.frame = LabelFrame(self.root, text="Enter server address")
        self.chat = Text(self.frame)
        self.client = client.Client()

    def start(self):
        self.frame.pack(padx=5, pady=5, expand=1)
        sub_frame = Frame(self.frame)
        sub_frame.grid(row=0, column=0, sticky="w")
        notification = StringVar()
        notification_label = Label(self.root, textvariable=notification, fg="#f00")
        notification_label.pack()
        Label(sub_frame, text="Server IP-address:").grid(row=0, column=0, sticky="w")
        Label(sub_frame, text="Server port:").grid(row=1, column=0, sticky="w")
        Label(sub_frame, text='Username:').grid(row=2, column=0, sticky="w")

        serverIP_entry = Entry(sub_frame)
        serverPort_entry = Entry(sub_frame)
        username_entry = Entry(sub_frame)

        serverIP_entry.grid(row=0, column=1, padx=5, pady=5)
        serverPort_entry.grid(row=1, column=1, padx=5, pady=5)
        username_entry.grid(row=2, column=1, padx=5, pady=5)
        connect_button = Button(self.frame, text="Connect!",
                                command=lambda: self.try_conn(username_entry.get(),
                                                              (serverIP_entry.get(), int(serverPort_entry.get())),
                                                              notification, notification_label))
        connect_button.grid(row=1, column=0, padx=10, pady=10)

    def try_conn(self, name, adr, notification: StringVar, label: Label):
        try:
            self.client.connect2server(name, adr)
        except Exception as e:
            notification.set(str(e))
            return
        self.frame.destroy()
        label.destroy()
        self.frame = LabelFrame(self.root, text="Creating new chat")
        self.frame.pack(padx=5, pady=5, expand=1)
        btn1 = Button(self.frame, text="Connect to peer", command=self.connect2peer)
        btn2 = Button(self.frame, text="Wait for connection", command=self.wait)
        self.root.title("Your nickname: " + self.client.username)
        btn1.grid(row=0, column=0, padx=10, pady=10)
        btn2.grid(row=1, column=0, padx=10, pady=10)

    def connect2peer(self):
        self.frame.destroy()
        self.frame = LabelFrame(self.root, text="Enter peer name")
        self.frame.pack(padx=5, pady=5, expand=1)
        entry = Entry(self.frame)
        entry.grid(row=0, column=0, padx=10, pady=10)
        btn = Button(self.frame, text="send!", command=lambda: self.connect(entry.get()))
        btn.grid(row=0, column=1, padx=10, pady=10)

    def connect(self, name):
        if self.client.connect2peer(name):
            self.new_chat()
        return

    def wait(self):
        self.frame.destroy()
        self.frame = Frame()
        self.frame.pack(expand=1)
        Label(self.frame, text="Waiting...").pack()
        self.client.wait()
        self.new_chat()

    def new_chat(self):
        self.frame.destroy()
        frame_name = "Chat with " + self.client.peerName
        self.frame = LabelFrame(self.root, text=frame_name)
        self.frame.pack(padx=5, pady=5, expand=1, fill=BOTH)
        self.chat.grid(row=0, column=0, padx=5, pady=5)
        message = StringVar()
        entry = Entry(self.frame, textvariable=message)
        entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        btn = Button(self.frame, command=lambda: self.send(message), text="Send")
        btn.grid(row=2, column=0, padx=5, pady=5)
        self.root.after(1, lambda: self.client.listen(self.root, self.chat))

    def send(self, message: StringVar):
        self.client.send(message.get())
        message.set('')


if __name__ == "__main__":
    window = Tk()
    app = Messenger(window)
    app.start()

    window.mainloop()
