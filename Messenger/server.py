import socket

key_length = 256
users = []


def getuser(name: str) -> int:
    for i in range(len(users)):
        user_name, x, addr = users[i]
        if user_name == name:
            return i
    return -1


def send_user(host_socket: socket.socket, user_index):
    user_name, key, addr = users[user_index]
    a, b = key
    user_host, user_port = addr
    host_socket.send(a.to_bytes(key_length, byteorder='big', signed=False))
    host_socket.send(b.to_bytes(key_length, byteorder='big', signed=False))
    host_socket.send(user_host.encode("utf-8"))
    host_socket.send(user_port.to_bytes(16, byteorder='big', signed=False))


while True:
    sock = socket.socket()
    sock.bind(('', 9999))
    sock.listen(5)
    print("Waiting for a new connection...")
    conn, adr = sock.accept()
    ip, port = adr
    print("Connection was established with: " + str(ip) + ":" + str(port))
    conn_type = conn.recv(2)
    if conn_type == b'\x11\x11':
        print("Registering a new user")
        username = conn.recv(40).decode('utf-8')
        if getuser(username) < 0:
            conn.send(b'\x00\x00')
        else:
            conn.send(b'\x11\x11')
            e = int.from_bytes(conn.recv(key_length), byteorder='big', signed=False)
            n = int.from_bytes(conn.recv(key_length), byteorder='big', signed=False)
            users.append((username, (e, n), adr))
            print("New user added: " + username + ", key:")
            print("     e -> " + str(e))
            print("     n -> " + str(n))
        conn.close()
        sock.close()
    elif conn_type == b'\x55\x55':
        print("Public key request handling...")
        username = conn.recv(40).decode('utf-8')
        print(username)
        index = getuser(username)
        if index < 0:
            conn.send(b'\x00\x00')
            print("Didn't found such user...")
        else:
            conn.send(b'\x11\x11')
            print("Sending user data...")
            send_user(conn, index)
            print("Requested user was sent...")
        conn.close()
        sock.close()
    print("Closing connection...")
