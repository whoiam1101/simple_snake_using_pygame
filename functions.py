from random import randint
from pygame.locals import Rect
from pygame.draw import rect
from pygame import Surface

from constants import SNAKE_SPEED
from colors import SNAKE_COLOR, FOOD_COLOR, SCREEN_BACKGROUN_COLOR


def random_position(screen_width: int, screen_height: int, cell_size: int) -> tuple[int, int]:
    return randint(0, screen_width-cell_size), randint(0, screen_height-cell_size)


def move(snake_cells: list[Rect], direction: tuple[int, int]) -> None:
    for i in range(len(snake_cells) - 1, 0, -1):
        snake_cells[i].move_ip(snake_cells[i - 1].centerx - snake_cells[i].centerx,
                               snake_cells[i - 1].centery - snake_cells[i].centery)
    snake_cells[0].move_ip(SNAKE_SPEED*direction[0], SNAKE_SPEED*direction[1])


def draw(screen:Surface,snake_cells: list[Rect], food: Rect) -> None:
    screen.fill(SCREEN_BACKGROUN_COLOR)
    for snake_cell in snake_cells:
        rect(screen, SNAKE_COLOR, snake_cell)
    rect(screen, FOOD_COLOR, food)
