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

    def __init__(self, client_socket, udp_addr):
        self.client_socket = client_socket
        self.udp_addr = udp_addr
        self.display = pyautogui.size()

    def on_move(self, x, y):
        try:
            self.client_socket.sendto(f"pos {x / self.display[0]} {y / self.display[1]},".encode(), self.udp_addr)
        except OSError:
            return False

    def on_click(self, x, y, button, pressed):
        try:
            print(pressed)
            if pressed:
                self.client_socket.sendto(
                    f"click {x / self.display[0]} {y / self.display[1]} {convert_button(button)},".encode(),
                    self.udp_addr)
            else:
                self.client_socket.sendto(
                    f"release mouse {x / self.display[0]} {y / self.display[1]} {convert_button(button)},".encode(),
                    self.udp_addr)

        except OSError:
            return False

    def on_scroll(self, x, y, dx, dy):
        try:
            self.client_socket.sendto(f"scroll {dx * 10} {dy * 10},".encode(), self.udp_addr)
        except OSError:
            return False
