import random
import socket
import threading
from server_package import my_socket


class Server:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.server.listen(1)
        self.clients = []

    def accept(self):
        client_socket, client_address = self.server.accept()
        my_client = my_socket.Socket(client_socket)
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

    def session(self, my_client):
        while True:
            if my_client.can_start_session:
                data = my_client.recv(1046576)
                my_client.partner.send(data)

    def connect(self, pin, my_client):
        for client in self.clients:
            if my_client.connect(client, pin) == "ok":
                return "ok"
            elif my_client.connect(client, pin) == "You cant host and connect":
                return "You cant host and connect"
        return "not a matching password"

    def main_conversation(self, my_client):
        try:
            while True:
                request = my_client.recv(1024).decode()
                if request == "1":
                    my_client.become_host(self.create_password())
                    my_client.send(str(my_client.pin))
                elif request == "2":
                    my_client.stop_hosting()
                elif request == "3":
                    if my_client.start_hosting():
                        self.session(my_client)
                elif request == "4":
                    my_client.send(str(my_client.pin))
                elif request == "5":
                    self.clients.remove(my_client)
                    my_client.exit()
                elif "connect " in request:
                    response = self.connect(int(request.split(" ")[1]), my_client)
                    my_client.send(response)
                    if response == "ok":
                        self.session(my_client)
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
    server = Server("0.0.0.0", 666)
    print('server started')
    while True:
        accepted_client = server.accept()
        threading.Thread(target=server.main_conversation, args=(accepted_client,)).start()


if __name__ == '__main__':
    main()
