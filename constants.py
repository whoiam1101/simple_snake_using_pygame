import json


CONSTANTS_FILE: str = "constants.json"


def get_value(key: str) -> int:
    with open(CONSTANTS_FILE, 'r', encoding='utf-8') as constant_file:
        constant: dict[str, int] = json.load(constant_file)
        return constant[key]


MOVE_INTERVAL = lambda: get_value('MOVE_INTERVAL')
DEAD_INTERVAL = lambda: get_value('DEAD_INTERVAL')

CELL_SIZE   = lambda: get_value('CELL_SIZE')
GRID_WIDTH  = lambda: get_value('GRID_WIDTH')
GRID_HEIGHT = lambda: get_value('GRID_HEIGHT')

BEST_SCORE = lambda: get_value('BEST_SCORE')

SCREEN_WIDTH  = lambda: CELL_SIZE() * GRID_WIDTH()
SCREEN_HEIGHT = lambda: CELL_SIZE() * GRID_HEIGHT()

SCORE_TEXT_SIZE      = lambda: CELL_SIZE()
WIDGET_TEXT_SIZE     = lambda: CELL_SIZE() // 2
BEST_SCORE_TEXT_SIZE = lambda: CELL_SIZE() * 2
