# -*- coding:utf-8 -*-

import os
import time

from config_manager import load_config
from content_fetcher import download_page, parse_html
from logger_setup import logger
from qbittorrent_downloader import add_magnet, is_torrent_exists


def process_config_item(item):
    """Check and download the latest content for the specified item"""
    name = item.get('name')
    url = item.get('url')
    dest = os.path.join("/downloads/Series", name)

    logger.debug(f"Checking for updates: {name}")

    try:
        html = download_page(url)
        movies = parse_html(html)

        for movie_name, magnet in movies.items():
            if not is_torrent_exists(magnet):
                if add_magnet(magnet, movie_name, name, dest):
                    logger.debug(f"Added new item: {movie_name}")
                else:
                    logger.error(f"Failed to add item: {movie_name}")
            else:
                logger.debug(f"Item up to date: {movie_name}")
    except Exception as e:
        logger.error(f"Error processing item {name}: {e}", exc_info=True)


def main():
    try:
        while True:
            config = load_config()
            items = config.get("auto_download_items", [])

            if not items:
                logger.warning("No item to monitor in config file")
                time.sleep(10)
                continue

            logger.debug(
                f"Monitoring {len(items)} {"items" if len(items) > 1 else "item"}, checking every 10 minutes...")

            for item in items:
                process_config_item(item)

            logger.info(f"Sleeping for 10 minutes before next check...")
            time.sleep(600)  # Sleep for 10 minutes
    except KeyboardInterrupt:
        logger.info("Program stopped")


if __name__ == '__main__':
    main()
