import os
from time import sleep

from qbittorrentapi import Client

from logger_setup import logger

# Use logger with specific name for this module
module_logger = logger.getChild('qbittorrent')

result = []
_existing_magnets_cache = []

# Get connection details from environment variables with defaults
qb_host = os.environ.get('QB_HOST', 'http://localhost:8888')
qb_username = os.environ.get('QB_USERNAME', '')
qb_password = os.environ.get('QB_PASSWORD', '')
qb_verify_cert = os.environ.get(
    'QB_VERIFY_CERT', 'False').lower() in ('true', '1', 'yes')

# Configure client with proper SSL verification setting
client = Client(
    host=qb_host,
    username=qb_username,
    password=qb_password,
    VERIFY_WEBUI_CERTIFICATE=qb_verify_cert
)

# Try to connect and log success/failure
try:
    client.auth_log_in()
    module_logger.info(f"Successfully connected to qBittorrent at {qb_host}")
except Exception as e:
    module_logger.error(f"Failed to connect to qBittorrent: {e}")


def get_existing_magnets():
    """Get all existing magnet links"""
    try:
        torrents = client.torrents_info()
        existing_magnets_cache = [torrent["magnet_uri"] for torrent in torrents]
        module_logger.info(
            f"Fetched {len(existing_magnets_cache)} existing magnet links")
        return existing_magnets_cache
    except Exception as e:
        module_logger.error(
            f"Error getting existing magnets: {e}", exc_info=True)
        return []


def add_magnet(magnet, name, category, save_path):
    """Add magnet link to qBittorrent, set torrent name, category, and save path"""

    if is_torrent_exists(magnet):
        module_logger.info(f"Magnet link already exists: {name}")
        return False

    try:
        ret = client.torrents_add(
            urls=magnet,
            name=name,
            category=category,
            save_path=save_path,
            use_auto_torrent_management=False,
            is_skip_checking=False
        )

        if ret is not "Ok.":
            module_logger.error(
                f"Failed to add magnet link: {ret}", exc_info=True)
            return False

        sleep(1)
        module_logger.info(f"Added download: {name} -> {save_path}")
        return True
    except Exception as e:
        module_logger.error(
            f"Failed to add magnet link for {name}: {e}", exc_info=True)
        return False


def is_torrent_exists(magnet):
    """Check if torrent already exists"""
    global _existing_magnets_cache

    # First check cache
    if magnet in _existing_magnets_cache:
        return True

    # If not in cache, refresh the cache
    _existing_magnets_cache = get_existing_magnets()
    return magnet in _existing_magnets_cache
