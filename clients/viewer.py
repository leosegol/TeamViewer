import threading

import pynput
from PIL import Image
import matplotlib.pyplot as plt

from keyboard_funcs.keyboard import Keyboard
from mouse_funcs.mouse import Mouse


class ViewerClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def see_screen(self):

        while True:
            total_data = b''
            settings = self.client_socket.recv(1024).decode()
            mode, length, x, y = settings.split(", ")
            y, data = y.split(")")
            size = int(x[1:-1]), int(y[1:-1])
            length = int(length[1:-1])
            mode = mode[2:-1]
            if data:
                length -= len(data.encode())
                total_data += data.encode()
            while length > 0:
                data = self.client_socket.recv(length)
                length -= len(data)
                total_data += data
            if length < 0:
                total_data = total_data[:length]
            image = Image.frombytes(mode, size, total_data)
            image.show()

    def send_mouse_instructions(self):
        mouse = Mouse(self.client_socket)
        with pynput.mouse.Listener(on_move=mouse.on_move, on_click=mouse.on_click,
                                   on_scroll=mouse.on_scroll) as mouse_listener:
            mouse_listener.join()

    def send_keyboard_instructions(self):
        keyboard = Keyboard(self.client_socket)
        with pynput.keyboard.Listener(on_press=keyboard.on_press, on_release=keyboard.on_release) as keyboard_listener:
            keyboard_listener.join()

    def viewer_mode(self):
        threading.Thread(target=self.see_screen, args=()).start()
        threading.Thread(target=self.send_mouse_instructions, args=()).start()
        threading.Thread(target=self.send_keyboard_instructions, args=()).start()
