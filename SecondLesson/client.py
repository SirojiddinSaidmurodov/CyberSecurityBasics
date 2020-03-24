import socket

sock = socket.socket()
sock.connect(('localhost', 9999))
while True:
    print("Enter your message <type 'quit' for stopping process> :\n")
    message = input()
    try:
        number = int(message)
        sock.send(b'\x55\x55')
        numberB = number.to_bytes((number.bit_length() + 7) // 8, byteorder='little', signed=True)
        sock.send(len(numberB).to_bytes(1000, byteorder='big'))
        sock.send(numberB)
    except ValueError:
        if message == 'quit':
            sock.send(b'\x00\x00')
            break
        sock.send(b'\x11\x11')
        sock.send(len(message).to_bytes(1000, byteorder='big'))
        sock.send(bytes(message, "utf-8"))

sock.close()
