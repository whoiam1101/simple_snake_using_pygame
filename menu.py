import pygame
import pygame_menu

from colors import SCORE_TEXT_COLOR
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BEST_SCORE,
    BEST_SCORE_TEXT_SIZE,
    CELL_SIZE
)
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

    menu_menu.add.label(BEST_SCORE(),
                        font_size=BEST_SCORE_TEXT_SIZE(),
                        font_color=SCORE_TEXT_COLOR,
                        margin=(0, CELL_SIZE()))
    menu_menu.add.button('Play',     game)
    menu_menu.add.button('Settings', settings)
    menu_menu.add.button('Quit',     quit)

    menu_menu.mainloop(screen)
