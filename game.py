import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, MOVE_INTERVAL, DEAD_INTERVAL
from functions import random_position, move, draw, place_food, colinear_dirs
from enums import MoveResult


def game() -> None:
    # pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    snake_cells: list[tuple[int, int]]
    food: tuple[int, int]
    direction: tuple[int, int]
    dead: bool
    directions_queue: list[tuple[int, int]]
    running = True


    def fill_initials() -> None:
        nonlocal snake_cells, food, direction, dead, directions_queue
        snake_cells = [random_position(GRID_WIDTH - 1, GRID_HEIGHT - 1)]
        food = place_food(GRID_WIDTH - 1, GRID_HEIGHT - 1, snake_cells)
        direction = (0, 0)
        dead = False
        directions_queue = []


    fill_initials()

    while running:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    directions_queue.append((-1, 0))
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    directions_queue.append((1, 0))
                if event.key in (pygame.K_UP, pygame.K_w):
                    directions_queue.append((0, -1))
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    directions_queue.append((0, 1))

        while len(directions_queue) > 0 and colinear_dirs(direction, directions_queue[0]):
            directions_queue = directions_queue[1:]
        if len(directions_queue) > 0:
            direction = directions_queue[0]
            directions_queue = directions_queue[1:]

        next_cells, move_result = move(GRID_WIDTH, GRID_HEIGHT, snake_cells, direction, food)
        snake_cells = next_cells
        if move_result == MoveResult.ATE_FOOD:
            food = place_food(GRID_WIDTH - 1, GRID_HEIGHT - 1, snake_cells)
        elif move_result == MoveResult.HIT_TAIL or move_result == MoveResult.HIT_BORDER:
            dead = True

        draw(screen, snake_cells, food, CELL_SIZE, dead)
        pygame.display.flip()

        end_time = pygame.time.get_ticks()
        spent_time = end_time - start_time

        if dead:
            pygame.time.wait(DEAD_INTERVAL)
            fill_initials()
        elif spent_time < MOVE_INTERVAL:
            pygame.time.wait(MOVE_INTERVAL - spent_time)


    pygame.quit()
    exit()
