import random
import socket
import threading

from server_package import my_socket


class Server:
    def __init__(self, ip, tcp_port, udp_port, udp_connection_port):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server.bind((ip, tcp_port))
        self.tcp_server.listen(1)
        self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server.bind((ip, udp_port))
        self.udp_server_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server_connection.bind((ip, udp_connection_port))
        self.clients = []

    def accept(self):
        tcp_client_socket, client_address = self.tcp_server.accept()
        connect_msg, udp_addr = self.udp_server_connection.recvfrom(1024)
        print(connect_msg)
        my_client = my_socket.Socket(tcp_client_socket, udp_addr)
        self.clients.append(my_client)
        return my_client

    def create_password(self):
        passwords = []
        for client in self.clients:
            passwords.append(client.pin)
        while True:
            password = random.randint(1000, 9999)
            if password not in passwords:
                break
        return password

    def session(self):
        while True:
            data, addr = self.udp_server.recvfrom(65507)
            for client in self.clients:
                if client.udp_client_address == addr:
                    if client.can_start_session():
                        try:
                            self.udp_server.sendto(data, client.partner.udp_client_address)
                        except AttributeError:
                            continue

    def connect(self, pin, my_client):
        for client in self.clients:
            if my_client.connect(client, pin):
                return "ok"
        return "something went wrong"

    def main_conversation(self, my_client):
        try:
            while True:
                request = my_client.recv(1024).decode()
                if "instruction " in request:
                    request = request.split("instruction ")[1].split(",")[0]
                    if request == "1":
                        my_client.become_host(self.create_password())
                        my_client.send(str(my_client.pin))
                    elif request == "2":
                        my_client.stop_hosting()
                    elif request == "3":
                        if my_client.start_hosting():
                            my_client.send("ok")
                        my_client.send("something went wrong")
                    elif request == "4":
                        my_client.send(str(my_client.pin))
                    elif request == "5":
                        self.clients.remove(my_client)
                        my_client.exit()
                        break
                    elif "connect " in request:
                        response = self.connect(int(request.split(" ")[1]), my_client)
                        my_client.send(response)
        except ConnectionError:
            self.clients.remove(my_client)
            my_client.exit()


"""
1) become a host
2) stop hosting
3) start hosting
4) my pass
5) exit
commands: |connect <password>|
"""


def main():
    server = Server("0.0.0.0", 666, 420, 69)
    threading.Thread(target=server.session, args=()).start()
    print('server started')
    while True:
        accepted_client = server.accept()
        threading.Thread(target=server.main_conversation, args=(accepted_client,)).start()


if __name__ == '__main__':
    main()
