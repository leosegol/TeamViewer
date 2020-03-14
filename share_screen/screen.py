import tkinter as tk

from PIL import ImageTk


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(self.root)
        self.label.pack(side="bottom", fill="both", expand="yes")

    def update_window(self, image):
        img = ImageTk.PhotoImage(image)
        self.label.configure(image=img)
        self.label.Image = img
