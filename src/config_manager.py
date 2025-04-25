import os
import tomllib

from logger_setup import logger

# Use logger with specific name for this module
module_logger = logger.getChild('config')


def load_config():
    """Load auto download configuration from TOML file"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'config', 'auto_download.toml')
    module_logger.debug(f"Loading configuration from {config_path}")

    try:
        with open(config_path, 'rb') as f:  # Open in binary mode as required by tomllib
            config = tomllib.load(f)
            module_logger.info(
                f"Configuration loaded successfully with {len(config.get('auto_download_items', []))} items")
            return config
    except FileNotFoundError:
        module_logger.error(f"Config file not found: {config_path}")
        return {}
    except Exception as e:
        module_logger.error(f"Failed to load config file: {e}", exc_info=True)
        return {}
