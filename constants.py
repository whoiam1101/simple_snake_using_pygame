import json


CONSTANTS_FILE: str = "constants.json"


INITIAL_CONSTANTS: dict[str, int] = {
    "MOVE_INTERVAL": 300,
    "CELL_SIZE":     32,
    "GRID_WIDTH":    14,
    "GRID_HEIGHT":   14,
    "BEST_SCORE":    0,
    "FPS":           60
}


def get_value(key: str) -> int:
    try:
        with open(CONSTANTS_FILE, 'r', encoding='utf-8') as constant_file:
            constant: dict[str, int] = json.load(constant_file)
            return constant[key]
    except FileNotFoundError:
        with open(CONSTANTS_FILE, 'w+', encoding='utf-8') as constant_file:
            json.dump(INITIAL_CONSTANTS, constant_file, ensure_ascii=False, indent=4)

        return get_value(key)


MOVE_INTERVAL = lambda: get_value('MOVE_INTERVAL')

CELL_SIZE   = lambda: get_value('CELL_SIZE')
GRID_WIDTH  = lambda: get_value('GRID_WIDTH')
GRID_HEIGHT = lambda: get_value('GRID_HEIGHT')

BEST_SCORE = lambda: get_value('BEST_SCORE')

FPS = lambda: get_value('FPS')

SCREEN_WIDTH  = lambda: CELL_SIZE() * GRID_WIDTH()
SCREEN_HEIGHT = lambda: CELL_SIZE() * GRID_HEIGHT()

SCORE_TEXT_SIZE      = lambda: CELL_SIZE()
WIDGET_TEXT_SIZE     = lambda: CELL_SIZE() // 2
BEST_SCORE_TEXT_SIZE = lambda: CELL_SIZE() * 2
