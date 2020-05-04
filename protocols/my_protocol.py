import socket

MSG_LENGTH = 7


def send(client_socket, msg):
    length = str(len(msg)).zfill(MSG_LENGTH).encode()
    msg = length + msg
    print(msg)
    while msg:
        if len(msg) > 10000:
            client_socket.send(msg[0:10000])
        else:
            client_socket.send(msg)
            break
        msg = msg[10000:]


def receive(client_socket):
    length = client_socket.recv(MSG_LENGTH)
    msg = client_socket.recv(int(length))
    return msg
