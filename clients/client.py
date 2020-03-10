import socket

from clients.host import HostClient
from clients.viewer import ViewerClient

MAIN_MENU = """
 1) print all connected clients
 2) become a host
 3) stop hosting
 4) my stats
 5) exit
 commands: |connect <password>, start(has to be a host)|
 """


class Client:
    def __init__(self):
        self.client_socket = socket.socket()
        self.is_host = False

    def connect(self, ip, port):
        self.client_socket.connect((ip, port))

    def main_conversation(self):
        while True:
            print('\n\n\n', MAIN_MENU)
            opt = input('choose an option: ')
            self.client_socket.send(opt.encode())
            if opt == '1':
                print(self.client_socket.recv(1024).decode())
            elif opt == '2':
                self.is_host = True
                print(f'Host mode is activated(pass={self.client_socket.recv(1024).decode()})')
            elif opt == '3':
                self.is_host = False
                print('you stopped hosting')
            elif opt == '4':
                print(self.client_socket.recv(1024).decode())
            elif opt == '5' or opt.lower() == 'exit':
                break
            elif 'start' in opt and self.is_host:
                HostClient(self.client_socket).host_mode()
            elif 'connect' in opt and not self.is_host:
                response = self.client_socket.recv(1024).decode()
                if response == 'ok':
                    ViewerClient(self.client_socket).viewer_mode()
                else:
                    print(response)
            input('press enter to continue...')


def main():
    client = Client()
    client.connect('10.0.0.4', 666)  # this stats later will be taken from the list (local_servers())
    client.main_conversation()
    client.client_socket.close()


if __name__ == '__main__':
    main()
