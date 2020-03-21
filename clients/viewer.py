import threading
import os
import pygame
import pynput

from keyboard_funcs.keyboard import Keyboard
from mouse_funcs.mouse import Mouse
from share_screen.screen import Window

FPS = 24
CAPTURE_EVERY = int(1000 / FPS)


class ViewerClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def see_screen(self):
        clicked = False
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        while True:
            total_data = b''
            settings = self.client_socket.recv(1024)
            mode, length, x, y = settings.split(b", ")
            y, data = y.split(b")")
            size = int(x[1:-1].decode()), int(y[1:-1].decode())
            length = int(length[1:-1].decode())
            mode = mode[2:-1].decode()
            if data:
                length -= len(data)
                total_data += data
            while length > 0:
                data = self.client_socket.recv(length)
                length -= len(data)
                total_data += data
            if length < 0:
                total_data = total_data[:length]
            image = pygame.image.fromstring(total_data, size, mode)
            display_surface = pygame.display.set_mode(image.get_size())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    clicked = True
            if not clicked:
                display_surface.blit(image, (0, 0))
                pygame.display.update()
            else:
                break

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
        self.see_screen()

        """ global app
        '''app.root.bind("<Motion>", self.see_screen)
        app.root.bind("<Motion>", self.see_screen)
        app.root.bind("<Motion>", self.see_screen)'''
        app.root.after(CAPTURE_EVERY, self.see_screen)
        app.root.mainloop()"""
