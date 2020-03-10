import pyautogui
from pynput.mouse import Button


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
        self.client_socket.send(f"pos {x / self.display[0]} {y / self.display[1]},".encode())

    def on_click(self, x, y, button, pressed):
        self.client_socket.send(f"click {x / self.display[0]} {y / self.display[1]} {convert_button(button)},".encode())

    def on_scroll(self, x, y, dx, dy):
        self.client_socket.send(f"scroll {dx} {dy},".encode())
