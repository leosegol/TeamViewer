import threading

import d3dshot
import pyautogui


class HostClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.display = pyautogui.size()

    def execute_instructions(self):
        pyautogui.FAILSAFE = False
        data = self.client_socket.recv(1024).decode()
        data = data.split(",")[0]
        if "pos" in data:
            x, y = data.split("pos ")[1].split(" ")
            pyautogui.moveTo(int(float(x) * self.display[0]), int(float(y) * self.display[1]))
        elif "click" in data:
            x, y, button = data.split("click ")[1].split(" ")
            pyautogui.click(int(float(x) * self.display[0]), int(float(y) * self.display[1]),
                            button=button)
        elif "scroll" in data:
            dx, dy = data.split("scroll ")[1].split(" ")
            pyautogui.scroll(int(dy))
            pyautogui.hscroll(int(dx))
        elif "press" in data:
            key = data.split("press ")[1]
            pyautogui.press(key)
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
                self.client_socket.send(str((pic.mode, str(len(data)), str(pic.size[0]), str(pic.size[1]))).encode())
                self.client_socket.sendall(data)

    def host_mode(self):
        threading.Thread(target=self.send_screen, args=()).start()
        while True:
            self.execute_instructions()
