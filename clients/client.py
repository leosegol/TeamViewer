import socket

from clients.host import HostClient
from clients.viewer import ViewerClient
from protocols.my_protocol import send as my_send
from protocols.my_protocol import receive as my_receive

MAIN_MENU = """
 1) become a host
 2) stop hosting
 3) start hosting
 4) my pass
 5) exit
 commands: |connect <password>|
 """


class Client:
    def __init__(self):
        self.client_socket = socket.socket()

    def connect(self, ip, port):
        self.client_socket.connect((ip, port))

    def main_conversation(self, recv_client):
        while True:
            print('\n\n\n', MAIN_MENU)
            opt = input('choose an option: ')
            my_send(self.client_socket, opt.encode())
            if opt == '1':
                print(f"Your pass: {my_receive(self.client_socket).decode()}")
            elif opt == '3':
                response = my_receive(self.client_socket).decode()
                print(response)
                if "ok" in response:
                    HostClient(self.client_socket, recv_client.client_socket).host_mode()
                    my_send(self.client_socket, "stop Share".encode())
            elif opt == '4':
                password = my_receive(self.client_socket).decode()
                if password != "-1":
                    print(f"Your password is {password}")
                else:
                    print("You must be a host")
            elif opt == '5':
                break
            elif 'connect' in opt:
                response = my_receive(self.client_socket).decode()
                if response == 'ok':
                    print("Wait for host to start the conversation")
                    ViewerClient(self.client_socket, recv_client.client_socket).viewer_mode()
                else:
                    print(response)
            input('press any key to continue...')


def main():
    client = Client()
    recv_client = Client()
    client.connect('127.0.0.1', 666)
    recv_client.connect('127.0.0.1', 667)
    client.main_conversation(recv_client)


if __name__ == '__main__':
    main()