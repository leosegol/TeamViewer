from time import time

import d3dshot
from PIL import ImageTk

from share_screen.screen import Window


def create_gui(window):
    window.create_button("become a host")
    window.create_button("stop hosting")
    window.create_button("start hosting")
    window.create_button("my pass")
    window.create_button("exit")
    window.create_textbox("connect ")



def main():
    app = Window()
    create_gui(app)
    app.root.mainloop()


if __name__ == '__main__':
    main()
