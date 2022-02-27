import os
from pathlib import Path
import requests
import logging
import parser

BASE_DIR = Path(__file__).resolve().parent
SITEMAP_PATH = f'{BASE_DIR}/sitemaps/main_sitemap.xml'
MAIN_SITEMAP_URL = 'https://aviapages.com/sitemap.xml'

logging.basicConfig(level=logging.INFO)


def main():

    # Download main sitemap
    download_main_sitemap()

    # Getting all links from the sitemap
    all_links = parser.get_sitemap_links(SITEMAP_PATH)

    # Running tests
    parser.run_test(all_links,
                    int(os.environ.get('RETRIES_COUNT')),
                    False)


def download_main_sitemap() -> None:

    logger = logging.getLogger('DOWNLOADER')
    logger.info('Downloading SITEMAP file...')

    headers = parser.generate_headers()
    request = requests.get(MAIN_SITEMAP_URL, headers=headers)
    with open(SITEMAP_PATH, 'w') as file:
        file.write(request.text)

    logger.info(f'Sitemap file created at {SITEMAP_PATH}')


if __name__ == '__main__':
    main()
