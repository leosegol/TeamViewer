import socket

MSG_LENGTH = 7


def send(client_socket, msg):
    client_socket.send(str(len(msg)).zfill(MSG_LENGTH).encode())
    while msg:
        if len(msg) > 100000:
            length = str(len(msg[0:100000])).zfill(MSG_LENGTH).encode()
            send_ = length + msg[0:100000]
            client_socket.send(send_)
        else:
            length = str(len(msg)).zfill(MSG_LENGTH).encode()
            send_ = length + msg
            client_socket.send(send_)
            break
        msg = msg[100000:]


def receive(client_socket):
    added_length = 0
    total_msg = b""
    total_length = client_socket.recv(MSG_LENGTH)
    print(total_length)
    while added_length < int(total_length):
        length = client_socket.recv(MSG_LENGTH)
        msg = client_socket.recv(int(length))
        added_length += int(length)
        total_msg += msg
    return total_msg
