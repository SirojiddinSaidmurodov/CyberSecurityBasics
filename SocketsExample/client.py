import socket

sock = socket.socket()
sock.connect(('localhost', 9999))
while True:
    print("Enter your message <type 'quit' for stopping process> :")
    message = input()
    try:
        number = int(message)
        sock.send(b'\x55\x55')
        numberB = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big', signed=True)
        sock.send(len(numberB).to_bytes(1000, byteorder='big'))
        sock.send(numberB)
    except ValueError:
        if message == 'quit':
            sock.send(b'\x00\x00')
            break
        sock.send(b'\x11\x11')
        messageB = message.encode("utf-8")
        sock.send(len(messageB).to_bytes(1000, byteorder='big'))
        sock.send(messageB)

sock.close()
