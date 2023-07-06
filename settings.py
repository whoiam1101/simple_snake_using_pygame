import pygame
import pygame_menu
import json

from constants import (
    CONSTANTS_FILE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from theme import theme


def set_value(key: str, value: int) -> None:
    with open(CONSTANTS_FILE, 'w') as constant_file:
        constant: dict[str, int] = json.load(constant_file)
        constant[key] = value
        json.dump(constant, constant_file)


def set_difficulty(difficulty: str) -> None:
    move_interval: dict[str, int] = {
        "EASY":        100,
        "MEDIUM":      150,
        "HARD":        200,
        "VERY HARD":   250,
        "IMMPOSSIBLE": 300
    }
    set_value('MOVE_INTERVAL', move_interval[difficulty])


def set_cell_size(value: str) -> None:
    set_value("CELL_SIZE", int(value))


def set_grid_size(value: str) -> None:
    value = int(value)
    set_value("GRID_WIDTH",  value)
    set_value("GRID_HEIGHT", value)


POSSIBLE_DIFFICULTY_VALUES: list[str] = ["EASY", "MEDIUM", "HARD", "VERY HARD", "IMMPOSSIBLE"]
POSSIBLE_CELL_SIZE_VALUES: list[str]  = ["8", "16", "32", "64"]
POSSIBLE_GRID_SIZE_VALUES: list[str]  = list(map(str, range(10, 21)))


def settings() -> None:
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH(), SCREEN_HEIGHT()))

    settings_menu: pygame_menu.Menu = pygame_menu.Menu('Snake',
                                                  width=SCREEN_WIDTH(),
                                                  height=SCREEN_HEIGHT(),
                                                  theme=theme)

    settings_menu.add.selector('Difficulty', POSSIBLE_DIFFICULTY_VALUES, onchange=set_difficulty)
    settings_menu.add.selector('Cell size',  POSSIBLE_CELL_SIZE_VALUES,  onchange=set_cell_size)
    settings_menu.add.selector('Grid size',  POSSIBLE_GRID_SIZE_VALUES,  onchange=set_grid_size)
    settings_menu.add.button('Back',         pygame.quit)

    settings_menu.mainloop(screen)

