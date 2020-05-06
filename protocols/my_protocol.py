import socket

MSG_LENGTH = 7


def send(client_socket, msg):
    try:
        client_socket.send(msg)
    except Exception:
        pass


def receive(client_socket, length):
    try:
        msg = client_socket.recv(length)
        return msg
    except Exception:
        pass
