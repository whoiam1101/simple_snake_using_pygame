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
    # read
    with open(CONSTANTS_FILE, 'r', encoding='utf-8') as constant_file:
        constant: dict[str, int] = json.load(constant_file)

    # change
    constant[key] = value

    # write
    with open(CONSTANTS_FILE, 'w', encoding='utf-8') as constant_file:
        json.dump(constant, constant_file, ensure_ascii=False, indent=4)


def set_difficulty(selected_difficulty: tuple[tuple[str, str], int], *args, **kwargs) -> None:
    selected_difficulty = selected_difficulty[0][0]
    move_interval: dict[str, int] = {
        "EASY":        300,
        "MEDIUM":      222,
        "HARD":        123,
        "VERY HARD":   100,
        "IMMPOSSIBLE": 75
    }
    set_value('MOVE_INTERVAL', move_interval[selected_difficulty])


def set_cell_size(selected_value: tuple[tuple[str, str], int], *args, **kwargs) -> None:
    set_value("CELL_SIZE", int(selected_value[0][0]))


def set_grid_size(selected_value: tuple[tuple[str, str], int], *args, **kwargs) -> None:
    selected_value = int(selected_value[0][0])
    set_value("GRID_WIDTH",  selected_value)
    set_value("GRID_HEIGHT", selected_value)


def selectorValuesMap(vals: list[str]) -> list[tuple[str, str]]:
    return list(map(lambda s : (s, s), vals))

POSSIBLE_DIFFICULTY_VALUES: list[str] = selectorValuesMap(["EASY", "MEDIUM", "HARD", "VERY HARD", "IMMPOSSIBLE"])
POSSIBLE_CELL_SIZE_VALUES:  list[str] = selectorValuesMap(["8", "16", "32", "64"])
POSSIBLE_GRID_SIZE_VALUES:  list[str] = selectorValuesMap(list(map(str, range(10, 21))))


def settings() -> None:
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH(), SCREEN_HEIGHT()))

    settings_menu: pygame_menu.Menu = pygame_menu.Menu('Snake',
                                                       width=SCREEN_WIDTH(),
                                                       height=SCREEN_HEIGHT(),
                                                       theme=theme)

    settings_menu.add.selector('Difficulty', POSSIBLE_DIFFICULTY_VALUES, onchange=set_difficulty)
    settings_menu.add.selector('Cell size',  POSSIBLE_CELL_SIZE_VALUES,  onchange=set_cell_size)
    settings_menu.add.selector('Grid size',  POSSIBLE_GRID_SIZE_VALUES,  onchange=set_grid_size)
    settings_menu.add.button('Back',         lambda: settings_menu.disable())

    settings_menu.mainloop(screen)
