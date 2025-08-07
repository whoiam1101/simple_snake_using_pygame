"""This module handles the configuration of the application."""
from omegaconf import OmegaConf, DictConfig
import os

# Define paths for config files
CONFIG_DIR = os.path.dirname(__file__)
DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIR, "default.yaml")

def _load_config() -> DictConfig:
    """
    Loads the configuration from default YAML file.

    Returns:
        DictConfig: The loaded configuration object.
    """
    return OmegaConf.load(DEFAULT_CONFIG_PATH)

# Create a singleton config object
CONF: DictConfig = _load_config()
