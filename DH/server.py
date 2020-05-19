import socket

from DH.dh import DH

sock = socket.socket()
sock.bind(("", 9090))
sock.listen(1)
print("Server is working")
keygen = DH()
g, p, public_key = keygen.generate()
print("Keys generated:")
print("g: " + str(g))
print("p: " + str(p))
print("Public key: " + str(public_key))
conn, adr = sock.accept()
print("Connection established with " + str(adr))
conn.send(g.to_bytes(16, byteorder='big', signed=False))
conn.send(p.to_bytes(16, byteorder='big', signed=False))
conn.send(public_key.to_bytes(16, byteorder='big', signed=False))
peer_key = int.from_bytes(conn.recv(16), byteorder='big', signed=False)
print("Peer's public key: " + str(peer_key))
common_key = keygen.calc_common_key(peer_key)
print(common_key)
