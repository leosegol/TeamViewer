import random
import socket
import threading


def get_other(dict, x):
    if x in dict:
        return dict[x]
    for key in dict:
        if dict[key] == x:
            return key


class Server:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.server.listen(1)
        self.clients = {}
        self.hosts = {}
        self.sessions = {}
        self.started_hosts = []

    def accept(self):
        client_socket, client_address = self.server.accept()
        self.clients[client_socket] = client_address
        return client_socket

    def create_password(self):
        while True:
            password = random.randint(1000, 9999)
            if password not in self.hosts.values():
                break
        return password

    def session(self, client_socket):
        while True:
            data = client_socket.recv(1048576)
            if get_other(self.hosts, client_socket) in self.hosts and get_other(self.hosts,
                                                                                client_socket) not in self.started_hosts:
                continue
            get_other(self.sessions, client_socket).sendall(data)
            if "exit".encode() in data:
                break

    def main_conversation(self, client_socket):
        try:
            while True:
                request = client_socket.recv(1024).decode()
                if request == '1':  # print connected clients
                    client_socket.send(str(self.clients.values()).encode())
                elif request == '2':  # become a host
                    password = str(self.create_password())
                    client_socket.send(password.encode())
                    self.hosts[client_socket] = password
                elif request == '3':
                    if client_socket in self.started_hosts:
                        del self.started_hosts[client_socket]
                    del self.hosts[client_socket]
                elif request == '4':
                    msg = str('address: ' + str(self.clients[client_socket]))
                    if client_socket in self.hosts:
                        msg = msg + 'pass=' + str(self.hosts[client_socket])
                    client_socket.send(msg.encode())
                elif request == '5' or request.lower() == 'exit':
                    del self.clients[client_socket]
                    if client_socket in self.hosts:
                        del self.sessions[client_socket]
                        del self.hosts[client_socket]
                    elif client_socket in self.sessions.values():
                        del self.sessions[client_socket]
                    client_socket.close()
                    break
                elif 'connect' in request and client_socket not in self.hosts:  # ...
                    try:
                        password = request.split('connect ')[1]
                        host = get_other(self.hosts, password)
                        self.sessions[host] = client_socket
                        client_socket.send("ok".encode())
                        self.session(client_socket)
                    except Exception:
                        client_socket.send('something went wrong...'.encode())
                elif request == 'start' and client_socket in self.hosts:
                    self.started_hosts.append(client_socket)
                    self.session(client_socket)
        except ConnectionError:
            del self.clients[client_socket]
            if client_socket in self.hosts:
                del self.sessions[client_socket]
                del self.hosts[client_socket]
            elif client_socket in self.sessions.values():
                del self.sessions[client_socket]
            client_socket.close()


def main():
    server = Server("0.0.0.0", 666)
    print('server is listening')
    while True:
        accepted_client = server.accept()
        threading.Thread(target=server.main_conversation, args=(accepted_client,)).start()


if __name__ == '__main__':
    main()
