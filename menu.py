"""
This module creates the main menu for the game.
"""
import pygame
import pygame_menu

from colors import SCORE_TEXT_COLOR
from config import CONF
from theme import theme
from quit import quit
from game import game
from settings import settings

def menu() -> None:
    """
    Creates and displays the main menu.
    """
    screen_width = CONF.game.cell_size * CONF.game.grid_width
    screen_height = CONF.game.cell_size * CONF.game.grid_height
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))

    menu_menu: pygame_menu.Menu = pygame_menu.Menu('Snake',
                                                   width=screen_width,
                                                   height=screen_height,
                                                   theme=theme)

    best_score_text = f"Best score: {CONF.game.best_score}"
    best_score_text_size = CONF.game.cell_size * 2
    cell_size = CONF.game.cell_size

    menu_menu.add.label(best_score_text,
                        font_size=best_score_text_size,
                        font_color=SCORE_TEXT_COLOR,
                        margin=(0, cell_size))
    menu_menu.add.button('Play', game)
    menu_menu.add.button('Settings', settings)
    menu_menu.add.button('Quit', quit)

    menu_menu.mainloop(screen)
