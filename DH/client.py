import socket

from DH.dh import DH

keygen = DH()
sock = socket.socket()
sock.connect(("localhost", 9090))
g = int.from_bytes(sock.recv(16), byteorder='big', signed=False)
p = int.from_bytes(sock.recv(16), byteorder='big', signed=False)
peer_key = int.from_bytes(sock.recv(16), byteorder='big', signed=False)
print("Keys received:")
print("g: " + str(g))
print("p: " + str(p))
print("Peer's key: " + str(peer_key))
public_key = keygen.calc_public_key(g, p)
sock.send(public_key.to_bytes(16, byteorder='big', signed=False))
print("Public key: " + str(public_key))
common_key = keygen.calc_common_key(peer_key)
print(common_key)
