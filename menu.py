import pygame
import pygame_menu

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import game


def quit() -> None:
    pygame_menu.events.EXIT


pygame.init()
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


menu: pygame_menu.Menu = pygame_menu.Menu('Hi Ilya',
                                          width=SCREEN_WIDTH,
                                          height=SCREEN_HEIGHT,
                                          theme=pygame_menu.themes.THEME_DARK)

menu.add.button('Play', game)
menu.add.button('Quit', quit)

menu.mainloop(screen)
