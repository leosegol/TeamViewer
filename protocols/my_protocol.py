import socket

MSG_LENGTH = 7


def send(client_socket, msg):

    while msg:
        if len(msg) > 10000:
            length = str(len(msg)).zfill(MSG_LENGTH).encode()
            send_ = length + msg[0:10000]
            client_socket.send(send_)
        else:
            length = str(len(msg)).zfill(MSG_LENGTH).encode()
            send_ = length + msg
            client_socket.send(send_)
            break
        msg = msg[10000:]


def receive(client_socket):
    length = client_socket.recv(MSG_LENGTH)
    msg = client_socket.recv(int(length))
    return msg
