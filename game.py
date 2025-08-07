"""
This module contains the main game logic.
"""
import pygame
from pygame_menu.font import FONT_8BIT

from colors import SCORE_TEXT_COLOR, SCREEN_BACKGROUND_COLOR
from config import CONF
from quit import quit
from snake import Snake

def game(screen: pygame.Surface) -> None:
    """
    Initializes and runs the main game loop.
    """
    pygame.font.init()

    screen_width, screen_height = screen.get_size()

    score_text_size = CONF.game.cell_size
    font = pygame.font.Font(FONT_8BIT, score_text_size)
    running: bool = True

    fps = CONF.game.fps
    cell_size = CONF.game.cell_size
    move_interval = CONF.game.move_interval
    grid_width = screen_width // cell_size
    grid_height = screen_height // cell_size

    clock = pygame.time.Clock()

    snake = Snake(grid_width, grid_height, screen, cell_size)

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

        if snake.score > CONF.game.best_score:
            CONF.game.best_score = snake.score

        screen.fill(SCREEN_BACKGROUND_COLOR)
        snake.draw()
        score_text = font.render(f'{snake.score}', True, SCORE_TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    quit()
