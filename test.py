import d3dshot
from PIL import ImageTk

from share_screen.screen import Window


def change(e):
    image = None

    if image != cam.get_latest_frame():
        image = cam.get_latest_frame()
        img = ImageTk.PhotoImage(image)
        app.label.configure(image=img)
        app.label.image = img


cam = d3dshot.create()
app = Window()


def main():
    global cam, app
    b = d3dshot.create()
    cam.capture(target_fps=1)
    app.root.bind("<Motion>", change)
    app.root.mainloop()


if __name__ == '__main__':
    main()
