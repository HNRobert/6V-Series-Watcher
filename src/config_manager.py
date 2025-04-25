import os
import tomllib


def load_config():
    """Load auto download configuration from TOML file"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'config', 'auto_download.toml')
    try:
        with open(config_path, 'rb') as f:  # Open in binary mode as required by tomllib
            return tomllib.load(f)
    except Exception as e:
        print(f"Failed to load config file: {e}")
        return {}
