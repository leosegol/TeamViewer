class Keyboard:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def on_press(self, key):
        self.client_socket.send(f"press {key},".encode())

    def on_release(self, key):
        self.client_socket.send(f"release {key},".encode())
