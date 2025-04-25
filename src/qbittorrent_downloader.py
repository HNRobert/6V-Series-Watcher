import os
from qbittorrentapi import Client
from time import sleep

result = []
_existing_magnets_cache = []
client = Client(host='http://localhost:8888', username='',
                password='')


def qbittorrent_open(path):
    a = open(path, 'rb')
    client.torrents_add(torrent_files=a, save_path='/home/hwm/torrents/')

    sleep(1)
    print(path, 'Success...')


def get_existing_magnets():
    """Get all existing magnet links"""
    global _existing_magnets_cache
    torrents = client.torrents_info()
    _existing_magnets_cache = [torrent.magnet_uri for torrent in torrents]
    return _existing_magnets_cache


def add_magnet(magnet, name, category, save_path):
    """Add magnet link to qBittorrent, set torrent name, category, and save path"""

    if is_torrent_exists(magnet):
        print(f"Magnet link already exists: {name}")
        return False

    # Uncomment the following line to add the magnet link to qBittorrent

    # client.torrents_add(
    #     urls=magnet,
    #     name=name,
    #     category=category,
    #     tags="Series",
    #     save_path=save_path,
    #     use_auto_torrent_management=False,
    #     is_skip_checking=False
    # )

    sleep(1)
    print(f"Added download: {name} -> {save_path}")
    return True


def is_torrent_exists(magnet):
    """Check if torrent already exists"""
    global _existing_magnets_cache

    # First check cache
    if magnet in _existing_magnets_cache:
        return True

    # If not in cache, refresh the cache
    _existing_magnets_cache = get_existing_magnets()
    return magnet in _existing_magnets_cache
