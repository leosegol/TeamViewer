import pyautogui
import pygame
from pynput.mouse import Button

from protocols.my_protocol import send as my_send


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
            x, y = pygame.mouse.get_pos()
        except Exception:
            pass
        try:
            my_send(self.client_socket, f"pos {x} {y},".encode())
        except OSError:
            return False

    def on_click(self, x, y, button, pressed):
        try:
            x, y = pygame.mouse.get_pos()
        except Exception:
            pass
        try:
            if pressed:
                my_send(self.client_socket,f"click {x} {y} {convert_button(button)},".encode())
            else:
                my_send(self.client_socket, f"release mouse {x} {y} {convert_button(button)},".encode())
        except OSError:
            return False

    def on_scroll(self, x, y, dx, dy):
        if pygame.display.get_active():
            try:
                my_send(self.client_socket, f"scroll {dx * 10} {dy * 10},".encode())
            except OSError:
                return False
