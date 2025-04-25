import hashlib
import os
import tomllib

from logger_setup import logger

# Use logger with specific name for this module
module_logger = logger.getChild('config')

# Store the previous file hash for comparison
_previous_file_hash = None


def load_config():
    """Load auto download configuration from TOML file"""
    global _previous_file_hash

    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'config', 'auto_download.toml')
    module_logger.debug(f"Loading configuration from {config_path}")

    try:
        # Calculate file hash to detect changes
        current_hash = calculate_file_hash(config_path)

        with open(config_path, 'rb') as f:
            config = tomllib.load(f)

        items = config.get('auto_download_items', [])
        items_count = len(items)
            
        # Check if the file has changed based on hash
        if _previous_file_hash is None:
            log_config_items(items, items_count, "Initial configuration loaded with")
        elif current_hash != _previous_file_hash:
            log_config_items(items, items_count, "Configuration file changed, now contains")
        else:
            module_logger.debug(f"Configuration unchanged with {items_count} items")

        # Update the previous hash
        _previous_file_hash = current_hash

        return config
    except FileNotFoundError:
        module_logger.error(f"Config file not found: {config_path}")
        return {}
    except Exception as e:
        module_logger.error(f"Failed to load config file: {e}", exc_info=True)
        return {}


def log_config_items(items, items_count, status):
    """Log configuration items with a status message"""
    # Collect log messages
    log_messages = [f"{status} {items_count} items"]
    
    # Add all item names to the log messages
    for item in items:
        if 'name' in item:
            log_messages.append(f" - {item['name']}")
    
    # Log all messages at once
    module_logger.info("\n".join(log_messages))


def calculate_file_hash(file_path):
    """Calculate MD5 hash of a file"""
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5()
            # Read file in chunks to handle large files efficiently
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
        return file_hash.hexdigest()
    except Exception as e:
        module_logger.error(f"Error calculating file hash: {e}")
        # Return a unique value to force reload on error
        return f"error_{os.urandom(8).hex()}"
