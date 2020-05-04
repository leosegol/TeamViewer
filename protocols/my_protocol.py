import socket

MSG_LENGTH = 7


def send(client_socket, msg):
    while msg:
        if len(msg) > 10000:
            client_socket.send(msg[0:10000])
        else:
            client_socket.send(msg)
            break
        msg = msg[10000:]


def receive(client_socket):
    msg = client_socket.recv(6220800)
    return msg
