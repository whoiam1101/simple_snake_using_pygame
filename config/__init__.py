"""
This package handles the configuration of the application.
"""
from .config import CONF, set_difficulty, set_cell_size, set_grid_size, save_config

__all__ = ["CONF", "set_difficulty", "set_cell_size", "set_grid_size", "save_config"]
