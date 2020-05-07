import socket
import constants.constants as con


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
