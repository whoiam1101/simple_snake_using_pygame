from pygame_menu import Theme
from pygame_menu.font import FONT_8BIT

from colors import SCREEN_BACKGROUND_COLOR
from constants import WIDGET_TEXT_SIZE


theme: Theme = Theme(background_color=SCREEN_BACKGROUND_COLOR,
                     border_color=SCREEN_BACKGROUND_COLOR,
                     cursor_color="green",
                     selection_color="green",
                     title=False,
                     widget_font=FONT_8BIT,
                     widget_font_size=WIDGET_TEXT_SIZE())
