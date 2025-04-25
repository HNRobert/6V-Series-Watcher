import os
import re
from time import sleep

from qbittorrentapi import Client

from logger_setup import logger

# Use logger with specific name for this module
module_logger = logger.getChild('qbittorrent')

result = []
# Store hashes instead of full magnet links for more efficient comparison
_existing_magnets_hash_cache = []

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
    """Get all existing magnet links as hash values"""
    try:
        torrents = client.torrents_info()
        # Extract and store only the hash values
        hashes = []
        for torrent in torrents:
            magnet = torrent.get("magnet_uri", "")
            hash_value = extract_hash_from_magnet(magnet)
            if hash_value:
                hashes.append(hash_value)

        module_logger.debug(f"Fetched {len(hashes)} existing torrent hashes")
        return hashes
    except Exception as e:
        module_logger.error(
            f"Error getting existing torrents: {e}", exc_info=True)
        return []


def add_magnet(magnet, name, category, save_path):
    """Add magnet link to qBittorrent, set torrent name, category, and save path"""
    try:
        ret = client.torrents_add(
            urls=magnet,
            name=name,
            category=category,
            save_path=save_path,
            use_auto_torrent_management=False,
            is_skip_checking=False
        )

        if ret != "Ok.":
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
    """Check if torrent already exists by comparing hash values"""
    global _existing_magnets_hash_cache

    # Extract hash from the magnet link
    magnet_hash = extract_hash_from_magnet(magnet)
    if not magnet_hash:
        module_logger.warning(f"Could not extract hash from magnet link")
        return False

    # First check hash cache directly
    if magnet_hash in _existing_magnets_hash_cache:
        return True

    # If not in cache, refresh the cache
    _existing_magnets_hash_cache = get_existing_magnets()

    # Check again with fresh cache
    return magnet_hash in _existing_magnets_hash_cache


def extract_hash_from_magnet(magnet):
    """Extract hash from a magnet link"""
    match = re.search(r'xt=urn:btih:([a-zA-Z0-9]+)', magnet)
    if match:
        return match.group(1).lower()
    return None

