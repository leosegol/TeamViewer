import threading

import d3dshot
import pyautogui

from protocols.my_protocol import receive as my_receive
from protocols.my_protocol import send as my_send


class HostClient:
    def __init__(self, send_socket, recv_socket):
        self.send_socket = send_socket
        self.recv_socket = recv_socket
        self.display = pyautogui.size()

    def execute_instructions(self):
        pyautogui.FAILSAFE = False
        while True:
            try:
                data = my_receive(self.recv_socket).decode()
            except ConnectionResetError:
                break
            data = data.split(",")[0]
            if "pos" in data:
                x, y = data.split("pos ")[1].split(" ")
                pyautogui.moveTo(int(float(x) * self.display[0]), int(float(y) * self.display[1]))
            elif "click" in data:
                x, y, button = data.split("click ")[1].split(" ")
                pyautogui.mouseDown(x=int(float(x) * self.display[0]), y=int(float(y) * self.display[1]),
                                    button=button)
            elif "release mouse" in data:
                x, y, button = data.split("release mouse ")[1].split(" ")
                pyautogui.mouseUp(x=int(float(x) * self.display[0]), y=int(float(y) * self.display[1]),
                                  button=button)
            elif "scroll" in data:
                dx, dy = data.split("scroll ")[1].split(" ")
                pyautogui.scroll(int(dy))
                pyautogui.hscroll(int(dx))
            elif "press" in data:
                key = data.split("press ")[1]
                pyautogui.keyDown(key)

            elif "release" in data:
                key = data.split("release ")[1]
                pyautogui.keyUp(key)

    def send_screen(self):
        cam = d3dshot.create()
        cam.capture(target_fps=24)
        while True:
            pic = cam.get_latest_frame()
            if pic:
                data = pic.tobytes()
                my_send(self.send_socket, str((pic.mode, pic.size)).encode())
                my_send(self.send_socket, data)
                print("Host", data)

    def host_mode(self):
        threading.Thread(target=self.send_screen, args=()).start()
        self.execute_instructions()
