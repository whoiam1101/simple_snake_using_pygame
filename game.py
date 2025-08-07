import pygame
from pygame_menu.font import FONT_8BIT

from colors import SCORE_TEXT_COLOR, SCREEN_BACKGROUND_COLOR
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    MOVE_INTERVAL,
    SCORE_TEXT_SIZE,
    FPS,
)

from quit import quit
from snake import Snake



def game() -> None:
    # pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH(), SCREEN_HEIGHT()))
    font = pygame.font.Font(FONT_8BIT, SCORE_TEXT_SIZE())
    running: bool = True

    fps = FPS()
    cell_size = CELL_SIZE()
    move_interval = MOVE_INTERVAL()

    clock = pygame.time.Clock()

    snake = Snake(GRID_WIDTH(), GRID_HEIGHT(), screen, cell_size)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.push_direction((-1, 0))
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.push_direction((1, 0))
                if event.key in (pygame.K_UP, pygame.K_w):
                    snake.push_direction((0, -1))
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.push_direction((0, 1))

        progress_step = clock.tick(fps) / move_interval
         
        snake.tick(progress_step)

        screen.fill(SCREEN_BACKGROUND_COLOR)
        snake.draw()
        score_text = font.render(f'{snake.score}', True, SCORE_TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    quit()
