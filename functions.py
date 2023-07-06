from random import randint
from pygame.locals import Rect
from pygame.draw import rect
from pygame import Surface

from colors import SNAKE_COLOR, FOOD_COLOR, SCREEN_BACKGROUND_COLOR, HEAD_COLOR, BORDER_COLOR, DEAD_COLOR
from enums import MoveResult


def random_position(top_x: int, top_y: int) -> tuple[int, int]:
    return randint(0, top_x), randint(0, top_y)

def place_food(top_x: int, top_y: int, exclude_cells: list[tuple[int, int]]) -> tuple[int, int]:
    while True:
        coordinates = (randint(0, top_x), randint(0, top_y))
        if not coordinates in exclude_cells:
            return coordinates


def move(grid_width: int, grid_height: int, snake_cells: list[tuple[int, int]], direction: tuple[int, int], food: tuple[int, int]) -> tuple[list[tuple[int, int]], MoveResult]:
    if direction == (0, 0):
        return snake_cells[:], MoveResult.OK
    n = len(snake_cells)
    head = snake_cells[n - 1]
    next_head = (head[0] + direction[0], head[1] + direction[1])
    if next_head[0] < 0 or next_head[1] < 0 or next_head[0] >= grid_width or next_head[1] >= grid_height:
        return snake_cells[:], MoveResult.HIT_BORDER
    for i in range(1, n):
        if snake_cells[i] == next_head:
            return snake_cells[:], MoveResult.HIT_TAIL
    if food == next_head:
        next_cells = snake_cells[:]
        next_cells.append(next_head)
        return next_cells, MoveResult.ATE_FOOD
    next_cells = snake_cells[1:]
    next_cells.append(next_head)
    return next_cells, MoveResult.OK


def draw(screen:Surface, snake_cells: list[tuple[int, int]], food: tuple[int, int], cell_size: int, dead: bool) -> None:
    screen.fill(SCREEN_BACKGROUND_COLOR)
    n = len(snake_cells)
    snake_color = SNAKE_COLOR
    head_color = HEAD_COLOR
    if dead:
        snake_color = head_color = DEAD_COLOR
    for i in range(0, n - 1):
        rect(screen, BORDER_COLOR, Rect(snake_cells[i][0] * cell_size, snake_cells[i][1] * cell_size, cell_size, cell_size))
        rect(screen, snake_color, Rect(snake_cells[i][0] * cell_size + 1, snake_cells[i][1] * cell_size + 1, cell_size - 2, cell_size - 2))
    rect(screen, BORDER_COLOR, Rect(snake_cells[n - 1][0] * cell_size, snake_cells[n - 1][1] * cell_size, cell_size, cell_size))
    rect(screen, head_color, Rect(snake_cells[n - 1][0] * cell_size + 1, snake_cells[n - 1][1] * cell_size + 1, cell_size - 2, cell_size - 2))
    rect(screen, BORDER_COLOR, Rect(food[0] * cell_size, food[1] * cell_size, cell_size, cell_size))
    rect(screen, FOOD_COLOR, Rect(food[0] * cell_size + 1, food[1] * cell_size + 1, cell_size - 2, cell_size - 2))


def colinear_dirs(dir1: tuple[int, int], dir2: tuple[int, int]) -> bool:
    return dir1 == dir2 or dir1 + dir2 == (0, 0)
