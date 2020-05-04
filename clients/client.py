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
        self.client_send = socket.socket()
        self.client_recv = socket.socket()

    def connect(self, ip, port1, port2):
        self.client_send.connect((ip, port1))
        self.client_recv.connect((ip, port2))

    def close(self):
        self.client_send.close()
        self.client_recv.close()

    def main_conversation(self):
        while True:
            print('\n\n\n', MAIN_MENU)
            opt = input('choose an option: ')
            my_send(self.client_send, opt.encode())
            if opt == '1':
                print(f"Your pass: {my_receive(self.client_recv, 1024).decode()}")
            elif opt == '3':
                response = my_receive(self.client_recv, 1024).decode()
                print(response)
                if "ok" in response:
                    HostClient(self.client_send, self.client_recv).host_mode()
            elif opt == '4':
                password = my_receive(self.client_recv, 1024).decode()
                if password != "-1":
                    print(f"Your password is {password}")
                else:
                    print("You must be a host")
            elif opt == '5':
                break
            elif 'connect' in opt:
                response = my_receive(self.client_recv, 1024).decode()
                if response == 'ok':
                    print("Wait for host to start the conversation")
                    ViewerClient(self.client_send, self.client_recv).viewer_mode()
                    self.close()
                    break
                else:
                    print(response)
            input('press any key to continue...')


def main():
    client = Client()
    client.connect('10.0.0.13', 666, 667)
    client.main_conversation()


if __name__ == '__main__':
    main()