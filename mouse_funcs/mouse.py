import pyautogui
from pynput.mouse import Button
import socket

def convert_button(button):
    if button == Button.left:
        return 'left'
    elif button == Button.right:
        return 'right'
    else:
        return 'middle'


class Mouse:

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.display = pyautogui.size()

    def on_move(self, x, y):
        try:
            self.client_socket.send(f"pos {x / self.display[0]} {y / self.display[1]},".encode())
        except OSError:
            pass

    def on_click(self, x, y, button, pressed):
        try:
            self.client_socket.send(f"click {x / self.display[0]} {y / self.display[1]} {convert_button(button)},".encode())
        except OSError:
            pass

    def on_scroll(self, x, y, dx, dy):
        try:
            self.client_socket.send(f"scroll {dx} {dy},".encode())
        except OSError:
            pass
