import socket

MSG_LENGTH = 7


def send(client_socket, msg):
    length = (str(len(msg)).zfill(MSG_LENGTH).encode())
    client_socket.sendall(length + msg)


def receive(client_socket):
    msg_length = client_socket.recv(MSG_LENGTH).decode()
    msg_length = int(msg_length)
    msg = client_socket.recv(msg_length)
    return msg
