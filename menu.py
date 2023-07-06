import pygame
import pygame_menu

from colors import SCREEN_BACKGROUN_COLOR
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import game


def quit() -> None:
    pygame_menu.events.EXIT


pygame.init()
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


menu_theme: pygame_menu.Theme = pygame_menu.Theme(background_color=SCREEN_BACKGROUN_COLOR,
                                                  border_color=SCREEN_BACKGROUN_COLOR,
                                                  cursor_color="green",
                                                  selection_color="green",
                                                  title=False,
                                                  # title_shadow=True,
                                                  widget_font=pygame_menu.font.FONT_8BIT)


menu: pygame_menu.Menu = pygame_menu.Menu('Snake',
                                          width=SCREEN_WIDTH,
                                          height=SCREEN_HEIGHT,
                                          theme=menu_theme)

menu.add.button('Play', game)
menu.add.button('Quit', quit)

menu.mainloop(screen)
