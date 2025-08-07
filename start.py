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
    menu()

if __name__ == "__main__":
    main()
