import random
import socket
import threading


from server_package import my_socket


def session(my_client):
    while True:
        if my_client.can_start_session():
            try:
                """
                data = my_receive(my_client.client_socket)
                print(data)
                my_send(my_client.client_socket, data)
                """
                data = my_client.recv()
                my_client.partner.send(data)
            except AttributeError:
                break


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

    def connect(self, pin, my_client):
        for client in self.clients:
            if my_client.connect(client, pin):
                return "ok"
        return "something went wrong"

    def main_conversation(self, my_client):
        try:
            while True:
                request = my_client.recv().decode()
                print(request)
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
                            session(my_client)
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
    server = Server("0.0.0.0", 666)
    print('server started')
    while True:
        accepted_client = server.accept()
        threading.Thread(target=server.main_conversation, args=(accepted_client,)).start()


if __name__ == '__main__':
    main()
