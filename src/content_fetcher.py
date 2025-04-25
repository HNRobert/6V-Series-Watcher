import bs4
import requests
from bs4 import BeautifulSoup

from logger_setup import logger

# Use logger with specific name for this module
module_logger = logger.getChild('fetcher')

COMMON_EXTENSIONS = ['.mp4', '.mkv', '.avi',
                     '.rmvb', '.flv', '.wmv', '.mov', '.3gp', '.ts']


def download_page(url):
    module_logger.debug(f"Downloading page: {url}")
    try:
        response = requests.get(url, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'})
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        module_logger.error(
            f"Failed to download page {url}: {e}", exc_info=True)
        raise


def parse_html(html):
    module_logger.debug("Parsing HTML content")
    try:
        # soup represents all the html statements in a static webpage
        soup = BeautifulSoup(html, 'lxml')
        a = soup.find('table', attrs={'cellspacing': '1'})
        if not a:
            module_logger.warning("No matching table found in HTML")
            return {}

        final = {}
        for movie_tr in a.find_all('tr'):
            name, magnet = fetch_movie_tr(movie_tr)
            if name and magnet:
                final[name] = magnet

        module_logger.debug(f"Found {len(final)} items in parsed content")
        return final
    except Exception as e:
        module_logger.error(f"Error parsing HTML: {e}", exc_info=True)
        return {}


def fetch_movie_tr(movie_tr: bs4.element.Tag) -> tuple:
    name = movie_tr.get_text().strip()

    if name.startswith('在线观看：', ):
        return None, None

    if name.startswith('磁力：'):
        name = name[3:]  # remove prefix

    for ext in COMMON_EXTENSIONS:
        if ext in name.lower():
            name = name.split(ext)[0]  # remove extension
            break

    anchor = movie_tr.find('a')
    if anchor and 'href' in anchor.attrs:
        magnet = anchor['href']
        return name, magnet
    return None, None
