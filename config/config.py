"""This module handles the configuration of the application."""
from collections.abc import Sequence
from omegaconf import OmegaConf, DictConfig
import os

# Define paths for config files
CONFIG_DIR = os.path.dirname(__file__)
DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIR, "default.yaml")
USER_CONFIG_PATH = os.path.join(CONFIG_DIR, "user.yaml")

def _load_config() -> DictConfig:
    """
    Loads the configuration from default and user YAML files.

    The user configuration is merged into the default configuration,
    overwriting any values that are present in both.

    Returns:
        DictConfig: The loaded configuration object.
    """
    # Load default config
    conf = OmegaConf.load(DEFAULT_CONFIG_PATH)

    # Load user config if it exists and merge it
    if os.path.exists(USER_CONFIG_PATH):
        user_conf = OmegaConf.load(USER_CONFIG_PATH)
        conf = OmegaConf.merge(conf, user_conf)

    return conf

def save_config(conf: DictConfig) -> None:
    """
    Saves the user-specific configuration.

    Only the parts of the configuration that differ from the default
    configuration are saved to the user's config file.

    Args:
        conf (DictConfig): The configuration object to save.
    """
    default_conf = OmegaConf.load(DEFAULT_CONFIG_PATH)
    user_conf = OmegaConf.create()

    # Find differences and save them
    for key, value in conf.game.items():
        if key not in default_conf.game or default_conf.game[key] != value:
            if 'game' not in user_conf:
                user_conf.game = {}
            user_conf.game[key] = value

    with open(USER_CONFIG_PATH, "w", encoding='utf-8') as f:
        OmegaConf.save(config=user_conf, f=f)

# Create a singleton config object
CONF: DictConfig = _load_config()

def set_difficulty(selected_difficulty: Sequence[Sequence[str]], *args, **kwargs) -> None:
    """
    Sets the move interval based on the selected difficulty.
    """
    if not selected_difficulty or not selected_difficulty[0]:
        return
    difficulty_str = selected_difficulty[0][0].lower().replace(" ", "_")
    if hasattr(CONF.difficulty, difficulty_str):
        move_interval = CONF.difficulty[difficulty_str]
        CONF.game.move_interval = move_interval
        save_config(CONF)

def set_cell_size(selected_value: Sequence[Sequence[str]], *args, **kwargs) -> None:
    """
    Sets the cell size in the configuration.
    """
    if not selected_value or not selected_value[0]:
        return
    try:
        CONF.game.cell_size = int(selected_value[0][0])
        save_config(CONF)
    except (ValueError, IndexError):
        pass

def set_grid_size(selected_value: Sequence[Sequence[str]], *args, **kwargs) -> None:
    """
    Sets the grid width and height in the configuration.
    """
    if not selected_value or not selected_value[0]:
        return
    try:
        size = int(selected_value[0][0])
        CONF.game.grid_width = size
        CONF.game.grid_height = size
        save_config(CONF)
    except (ValueError, IndexError):
        pass
