import threading

import d3dshot
import pynput
from PIL import Image, ImageTk

from keyboard_funcs.keyboard import Keyboard
from mouse_funcs.mouse import Mouse
from share_screen.screen import Window

app = Window()
FPS = 24
CAPTURE_EVERY = 1 / FPS


class ViewerClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def see_screen(self, e):
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

        img = ImageTk.PhotoImage(image)
        app.label.configure(image=img)
        app.label.image = img

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
        # threading.Thread(target=self.see_screen, args=()).start()
        mouse = threading.Thread(target=self.send_mouse_instructions, args=())
        keyboard = threading.Thread(target=self.send_keyboard_instructions, args=())
        mouse.start()
        keyboard.start()
        global app
        """app.root.bind("<Motion>", self.see_screen)
        app.root.bind("<Motion>", self.see_screen)
        app.root.bind("<Motion>", self.see_screen)"""
        app.root.after(CAPTURE_EVERY, self.see_screen)
        app.root.mainloop()
