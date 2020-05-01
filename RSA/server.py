import socket

sock = socket.socket()
sock.bind(('', 9999))
key_length = 512
users = []

while True:
    print("Waiting for new connection...")
    conn, adr = sock.accept()
    ip, port = adr
    print("Connection was established with: " + str(ip) + ":" + str(port))
    conn_type = conn.recv(2)
    if conn_type == b'\x11\x11':
        print("Registering a new user")
        username = conn.recv(40).decode('utf-8')
        e = int.from_bytes(conn.recv(key_length), byteorder='big', signed=False)
        n = int.from_bytes(conn.recv(key_length), byteorder='big', signed=False)
        users.append((username, (e, n)))
        print("New user added: " + username + ", key:")
        print("     e -> " + str(e))
        print("     n -> " + str(n))
    elif conn_type == b'\x55\x55':
        print("Public key request handling...")
        username = conn.recv(40).decode('utf-8')
    conn.close()
    print("Closing connection...")
