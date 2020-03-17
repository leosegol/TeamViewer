import pygame


def create_gui(window):
    window.create_button("become a host")
    window.create_button("stop hosting")
    window.create_button("start hosting")
    window.create_button("my pass")
    window.create_button("exit")
    window.create_textbox("connect ")


def main():
    pygame.init()
    image = pygame.image.load(r"C:\Users\Leo\Pictures\dissss.PNG")
    display_surface = pygame.display.set_mode(image.get_size())
    clicked = False
    while not clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                clicked = True
        if not clicked:
            display_surface.blit(image, (0, 0))


if __name__ == '__main__':
    main()
