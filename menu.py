import pygame
import pygame_menu

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from theme import theme

from quit import quit
from game import game
from settings import settings


def menu() -> None:
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH(), SCREEN_HEIGHT()))


    menu_menu: pygame_menu.Menu = pygame_menu.Menu('Snake',
                                            width=SCREEN_WIDTH(),
                                            height=SCREEN_HEIGHT(),
                                            theme=theme)

    menu_menu.add.button('Play',     game)
    menu_menu.add.button('Settings', settings)
    menu_menu.add.button('Quit',     quit)

    menu_menu.mainloop(screen)
