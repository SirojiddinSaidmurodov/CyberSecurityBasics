import socket

sock = socket.socket()
sock.bind(('', 9999))
sock.listen(1)
print("Server is working")
conn, adr = sock.accept()
ip, port = adr
print("Connection was established with: " + str(ip) + ':' + str(port))
while True:
    messageType = conn.recv(2)
    msgLen = int.from_bytes(conn.recv(1000), byteorder='big')
    if messageType == b'\x11\x11':
        print("Receiving string")
        message = conn.recv(msgLen)
        print(message.decode("utf-8"))
    elif messageType == b'\x55\x55':
        print("Receiving number")
        number = int.from_bytes(conn.recv(msgLen), byteorder='little', signed=True)
        print(number)
    elif messageType == b'\x00\x00':
        break

print("Shutting off")
conn.close()
