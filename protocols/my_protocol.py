import socket

MSG_LENGTH = 7


def send(client_socket, msg):
    client_socket.send(msg)


def receive(client_socket):
    msg = client_socket.recv(32768)
    return msg
