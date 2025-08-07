"""
This module creates the settings menu for the game.
"""
import pygame
import pygame_menu
from collections.abc import Mapping, Sequence

from config import CONF
from theme import theme
from config import set_difficulty, set_cell_size, set_grid_size

def selector_values_map(values: Sequence[str | int]) -> list[tuple[str, str]]:
    """
    Maps a sequence of values to a list of tuples for the pygame-menu selector.

    Args:
        values: A sequence of strings or integers.

    Returns:
        A list of tuples, where each tuple contains the string representation of the value.
    """
    return [(str(v), str(v)) for v in values]

def settings() -> None:
    """
    Creates and displays the settings menu.
    """
    screen_width = CONF.game.cell_size * CONF.game.grid_width
    screen_height = CONF.game.cell_size * CONF.game.grid_height
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))

    settings_menu: pygame_menu.Menu = pygame_menu.Menu('Snake',
                                                       width=screen_width,
                                                       height=screen_height,
                                                       theme=theme)

    possible_difficulty_values = selector_values_map(CONF.menu.difficulty_values)
    possible_cell_size_values = selector_values_map(CONF.menu.cell_size_values)
    possible_grid_size_values = selector_values_map(CONF.menu.grid_size_values)

    settings_menu.add.selector('Difficulty', possible_difficulty_values, onchange=set_difficulty, keyboard_selection=False)
    settings_menu.add.selector('Cell size',  possible_cell_size_values,  onchange=set_cell_size, keyboard_selection=False)
    settings_menu.add.selector('Grid size',  possible_grid_size_values,  onchange=set_grid_size, keyboard_selection=False)
    settings_menu.add.button('Back',         lambda: settings_menu.disable())

    settings_menu.mainloop(screen)
