"""
This module handles quitting the game.
"""
import pygame
import sys

def quit() -> None:
    """
    Quits the game.
    """
    pygame.quit()
    sys.exit()
