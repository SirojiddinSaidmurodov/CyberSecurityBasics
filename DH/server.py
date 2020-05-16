import socket

from DH.dh import DH

keygen = DH()
g, p, public_key = keygen.generate()
sock = socket.socket()
sock.bind(("", 9090))
sock.listen(1)
print("Server is working")
conn, adr = sock.accept()
print("Connection established with " + str(adr))
conn.send(g.to_bytes(16, byteorder='big', signed=False))
conn.send(p.to_bytes(16, byteorder='big', signed=False))
conn.send(public_key.to_bytes(16, byteorder='big', signed=False))
peer_key = int.from_bytes(conn.recv(16), byteorder='big', signed=False)
common_key = keygen.calc_common_key(peer_key)
print(common_key)
