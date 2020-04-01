
class Keyboard:

    def __init__(self, client_socket, udp_addr):
        self.client_socket = client_socket
        self.udp_addr = udp_addr

    def on_press(self, key):
        if "." in str(key):
            key = str(key).split(".")[1]
        else:
            key = str(key)[1:-1]
        try:
            self.client_socket.sendto(f"press {key},".encode(), self.udp_addr)
        except ConnectionResetError:
            return False

    def on_release(self, key):
        if "." in str(key):
            key = str(key).split(".")[1]
        else:
            key = str(key)[1:-1]
        try:
            self.client_socket.sendto(f"release {key},".encode(), self.udp_addr)
        except ConnectionResetError:
            return False
