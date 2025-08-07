"""
This is the main entry point for the application.
"""
import pygame

from menu import menu

def main() -> None:
    """
    Initializes pygame and starts the game menu.
    """
    pygame.init()
    pygame.display.set_caption("Snake Game")
    # Increase board size by 1.5 times
    screen = pygame.display.set_mode((1200, 900))
    menu(screen)

if __name__ == "__main__":
    main()
