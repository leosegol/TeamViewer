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
        self.client_socket = socket.socket()

    def connect(self, ip, port):
        self.client_socket.connect((ip, port))

    def main_conversation(self):
        while True:
            print('\n\n\n', MAIN_MENU)
            opt = input('choose an option: ')
            self.client_socket.send(f"instruction {opt},".encode())
            if opt == '1':
                print(f"Your pass: {self.client_socket.recv(1024).decode()}")
            elif opt == '3':
                response = self.client_socket.recv(1024).decode()
                print(response)
                if "ok" in response:
                    HostClient(self.client_socket).host_mode()
            elif opt == '4':
                password = self.client_socket.recv(1024).decode()
                if password != "-1":
                    print(f"Your password is {password}")
                else:
                    print("You must be a host")
            elif opt == '5':
                break
            elif 'connect' in opt:
                response = self.client_socket.recv(1024).decode()
                if response == 'ok':
                    print("Wait for host to start the conversation")
                    ViewerClient(self.client_socket).viewer_mode()
                else:
                    print(response)
            input('press any key to continue...')


def main():
    client = Client()
    client.connect('10.0.0.3', 666)  # this stats later will be taken from the list (local_servers())
    client.main_conversation()


if __name__ == '__main__':
    main()
