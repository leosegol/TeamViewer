import tkinter as tk

from PIL import ImageTk


class Window:
    def __init__(self, text=None):
        self.root = tk.Tk()
        self.label = tk.Label(self.root, text=text)
        self.label.pack(side="bottom", fill="both", expand="yes")
        self.buttons = {}
        self.text = tk.Text(self.root, height=1, width=20)

    def update_window(self, image):
        img = ImageTk.PhotoImage(image)
        self.label.configure(image=img)
        self.label.image = img

    def create_button(self, name):
        button = tk.Button(self.root, text=name)
        self.buttons[name] = button
        button.pack()

    def create_textbox(self, text):
        self.text.insert(tk.INSERT, text)
        self.text.pack()
