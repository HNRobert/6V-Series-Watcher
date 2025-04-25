# -*- coding:utf-8 -*-

import os
import time
from datetime import datetime

from config_manager import load_config
from content_fetcher import download_page, parse_html
from qbittorrent_downloader import add_magnet, is_torrent_exists

# Store processed magnet links
processed_magnets = set()


def process_config_item(item):
    """Check and download the latest content for the specified item"""
    name = item.get('name')
    url = item.get('url')
    dest = os.path.join("/downloads", name)

    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for updates: {name}")

    try:
        html = download_page(url)
        movies = parse_html(html)

        for movie_name, magnet in movies.items():
            if magnet not in processed_magnets and not is_torrent_exists(magnet):
                if add_magnet(magnet, movie_name, name, dest):
                    processed_magnets.add(magnet)
                    print(f"Added new item: {movie_name}")
            else:
                print(f"Item already exists: {movie_name}")
    except Exception as e:
        print(f"Error processing item {name}: {e}")


def main():
    try:
        while True:
            config = load_config()
            items = config.get("auto_download_items", [])

            if not items:
                print("No items to monitor in config file")
                time.sleep(10)
                continue

            print(f"Monitoring {len(items)} items, checking every minute...")

            for item in items:
                process_config_item(item)

            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sleeping for 10 minutes before next check...")
            time.sleep(600)  # Sleep for 10 minutes
    except KeyboardInterrupt:
        print("\nProgram stopped")


if __name__ == '__main__':
    main()
