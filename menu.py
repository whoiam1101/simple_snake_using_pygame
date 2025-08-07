"""
This module creates the main menu for the game.
"""
import pygame
import pygame_menu

from colors import SCORE_TEXT_COLOR
from config import CONF
from theme import theme
from quit import quit
from game import game
from high_scores import get_best_score, format_scores_for_display

def menu(screen: pygame.Surface) -> None:
    """
    Creates and displays the main menu.
    """
    screen_width, screen_height = screen.get_size()

    menu_menu: pygame_menu.Menu = pygame_menu.Menu('Snake',
                                                   width=screen_width,
                                                   height=screen_height,
                                                   theme=theme)

    # Get high scores from the new system
    best_score = get_best_score()
    best_score_text = f"Best score: {best_score}"
    best_score_text_size = CONF.game.cell_size * 2
    cell_size = CONF.game.cell_size

    menu_menu.add.label(best_score_text,
                        font_size=best_score_text_size,
                        font_color=SCORE_TEXT_COLOR,
                        margin=(0, cell_size))
    
    # Add high scores section
    menu_menu.add.label("HIGH SCORES",
                        font_size=cell_size,
                        font_color=SCORE_TEXT_COLOR,
                        margin=(0, cell_size//2))
    
    # Display top 5 scores with dates
    high_scores = format_scores_for_display()
    for score_line in high_scores:
        menu_menu.add.label(score_line,
                            font_size=cell_size//2,
                            font_color=SCORE_TEXT_COLOR,
                            margin=(0, 2))
    
    # Add instructions
    instructions = "Use ARROW KEYS or WASD to move. Press ESC to return to menu."
    menu_menu.add.label(instructions,
                        font_size=cell_size//2,
                        font_color=SCORE_TEXT_COLOR,
                        margin=(0, cell_size//2))
    
    menu_menu.add.button('Play', lambda: game(screen))
    menu_menu.add.button('Quit', quit)

    menu_menu.mainloop(screen)
