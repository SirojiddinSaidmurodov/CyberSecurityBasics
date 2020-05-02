import socket

sock = socket.socket()
sock.bind(('', 9999))
sock.listen(1)
print("Server is working")
conn, adr = sock.accept()
ip, port = adr
print("Connection was established with: " + str(ip) + ':' + str(port))
