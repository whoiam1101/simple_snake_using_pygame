from enum import Enum

class MoveResult(Enum):
    OK = 0
    ATE_FOOD = 1
    HIT_TAIL = 2
    HIT_BORDER = 3