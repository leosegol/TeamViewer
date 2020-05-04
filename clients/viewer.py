import threading
import os
import pygame
import pynput
import json
from keyboard_funcs.keyboard import Keyboard
from mouse_funcs.mouse import Mouse
from protocols.my_protocol import send as my_send
from protocols.my_protocol import receive as my_receive

FPS = 24
CAPTURE_EVERY = int(1000 / FPS)


class ViewerClient:
    def __init__(self, send_socket, recv_socket):
        self.send_socket = send_socket
        self.recv_socket = recv_socket

    def see_screen(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        while True:

            settings = my_receive(self.recv_socket)
            print(settings)
            c = settings.rsplit(b")")
            c[0] += b")"
            c[1] += b")"
            settings = c[0] + c[1]
            mode, size, data_len = eval(settings)
            total_data = c[2]
            total_data += my_receive(self.recv_socket)
            print("viewer", total_data)
            print(len(total_data), data_len)
            while len(total_data) < int(data_len):
                print(len(total_data))
                total_data += my_receive(self.recv_socket)
            total_data = total_data[0:data_len]
            image = pygame.image.fromstring(total_data, size, mode)
            display_surface = pygame.display.set_mode(image.get_size())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            else:
                display_surface.blit(image, (0, 0))
                pygame.display.update()
                continue
            break

    def send_mouse_instructions(self):
        mouse = Mouse(self.send_socket)
        with pynput.mouse.Listener(on_move=mouse.on_move, on_click=mouse.on_click,
                                   on_scroll=mouse.on_scroll) as mouse_listener:
            mouse_listener.join()

    def send_keyboard_instructions(self):
        keyboard = Keyboard(self.send_socket)
        with pynput.keyboard.Listener(on_press=keyboard.on_press, on_release=keyboard.on_release) as keyboard_listener:
            keyboard_listener.join()

    def viewer_mode(self):
        mouse = threading.Thread(target=self.send_mouse_instructions, args=())
        keyboard = threading.Thread(target=self.send_keyboard_instructions, args=())
        mouse.start()
        keyboard.start()
        self.see_screen()
