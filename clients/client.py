import socket

from clients.host import HostClient
from clients.viewer import ViewerClient
from share_screen.screen import Window

MAIN_MENU = """
 1) become a host
 2) stop hosting
 3) start hosting
 4) my pass
 5) exit
 commands: |connect <password>|
 """


def create_gui(window):
    window.create_button("become a host")
    window.create_button("stop hosting")
    window.create_button("start hosting")
    window.create_button("my pass")
    window.create_button("exit")


class Client:
    def __init__(self):
        self.tcp_client_socket = socket.socket()
        self.udp_client_socket = socket.socket()
        self.udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_addr = ()

    def connect(self, ip, tcp_port, udp_port, udp_connection):
        self.tcp_client_socket.connect((ip, tcp_port))
        self.udp_addr = (ip, udp_port)
        self.udp_client_socket.sendto("connect".encode(), (ip, udp_connection))

    def main_conversation(self):
        while True:
            print('\n\n\n', MAIN_MENU)
            opt = input('choose an option: ')
            self.tcp_client_socket.send(f"instruction {opt},".encode())
            if opt == '1':
                print(f"Your pass: {self.tcp_client_socket.recv(1024).decode()}")
            elif opt == '3':
                response = self.tcp_client_socket.recv(1024).decode()
                print(response)
                if "ok" in response:
                    HostClient(self.udp_client_socket, self.udp_addr).host_mode()
            elif opt == '4':
                password = self.tcp_client_socket.recv(1024).decode()
                if password != "-1":
                    print(f"Your password is {password}")
                else:
                    print("You must be a host")
            elif opt == '5':
                break
            elif 'connect' in opt:
                response = self.tcp_client_socket.recv(1024).decode()
                if response == 'ok':
                    print("Wait for host to start the conversation")
                    ViewerClient(self.udp_client_socket, self.udp_addr).viewer_mode()
                else:
                    print(response)
            input('press any key to continue...')


def main():
    client = Client()
    client.connect('127.0.0.1', 666, 420 ,69)  # this stats later will be taken from the list (local_servers())
    client.main_conversation()


if __name__ == '__main__':
    main()