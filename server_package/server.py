import random
import socket
import threading
import constants.constants as con
from server_package import my_socket


def session(client):
    while True:
        if client.can_start_session():
            try:
                data = client.recv()
                client.partner.send(data)
                if "STOP".encode() in data:
                    break
            except AttributeError:
                break


class Server:
    def __init__(self, ip, port1, port2):
        self.server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server1.bind((ip, port1))
        self.server1.listen(1)

        self.server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server2.bind((ip, port2))
        self.server2.listen(1)

        self.clients = []

    def accept(self):
        client_send, client_address = self.server1.accept()
        client_recv, client_address = self.server2.accept()
        my_client = my_socket.Socket(client_send, client_recv)
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

    def connect(self, pin, my_client):
        for client in self.clients:
            if my_client.connect(client, pin):
                return "ok"
        return "something went wrong"

    def main_conversation(self, my_client):
        try:
            while True:
                request = my_client.recv()
                print("main", request)
                request = request.decode()
                if request == "1":
                    my_client.become_host(self.create_password())
                    my_client.send(str(my_client.pin))
                elif request == "2":
                    my_client.stop_hosting()
                elif request == "3":
                    if my_client.start_hosting():
                        my_client.send("ok")
                        session(my_client)
                        continue
                    my_client.send("something went wrong")
                elif request == "4":
                    my_client.send(str(my_client.pin))
                elif request == "5":
                    self.clients.remove(my_client)
                    my_client.exit()
                    break
                elif "connect " in request:
                    try:
                        response = self.connect(int(request.split(" ")[1]), my_client)
                    except TypeError:
                        my_client.send("something went wrong")
                        continue
                    my_client.send(response)
                    if response == "ok":
                        session(my_client)
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
    server = Server(con.SERVER_IP, con.RECV_SOCKET_PORT, con.SEND_SOCKET_PORT)
    print('server started')
    print(socket.gethostbyname(socket.gethostname()))
    while True:
        client = server.accept()
        threading.Thread(target=server.main_conversation, args=(client, )).start()


if __name__ == '__main__':
    main()#ar
