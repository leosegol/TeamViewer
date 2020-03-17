
class Keyboard:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def on_press(self, key):
        if "." in str(key):
            key = str(key).split(".")[1]
        else:
            key = str(key)[1:-1]
        try:
            self.client_socket.send(f"press {key},".encode())
        except ConnectionResetError:
            return False

    def on_release(self, key):
        if "." in str(key):
            key = str(key).split(".")[1]
        else:
            key = str(key)[1:-1]
        try:
            self.client_socket.send(f"release {key},".encode())
        except ConnectionResetError:
            return False
