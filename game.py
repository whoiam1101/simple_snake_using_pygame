import pygame

from pygame.locals import Rect

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, FPS_LIMIT
from functions import random_position, move, draw


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
snake_cells: list[Rect] = [Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, CELL_SIZE, CELL_SIZE)]
food: Rect = Rect(*random_position(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE), CELL_SIZE, CELL_SIZE)
direction = (0, 0)
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                direction = (-1, 0)
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                direction = (1, 0)
            if event.key in (pygame.K_UP, pygame.K_w):
                direction = (0, -1)
            if event.key in (pygame.K_DOWN, pygame.K_s):
                direction = (0, 1)

    move(snake_cells, direction)

    if snake_cells[0].colliderect(food):
        food = Rect(*random_position(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE), CELL_SIZE, CELL_SIZE)
        snake_cells.append(snake_cells[-1].move(-CELL_SIZE*direction[0], -CELL_SIZE*direction[1]))

    if snake_cells[0].centerx in (0, SCREEN_WIDTH) or snake_cells[0].centery in (0, SCREEN_HEIGHT):
        running = False

    draw(screen, snake_cells, food)
    pygame.display.flip()
    clock.tick(FPS_LIMIT)


pygame.quit()
