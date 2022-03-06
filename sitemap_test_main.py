import os
from pathlib import Path
import logging
import requests

import parser
from parser import Parser

BASE_DIR = Path(__file__).resolve().parent
SITEMAP_PATH = f'{BASE_DIR}/sitemaps/main_sitemap.xml'
MAIN_SITEMAP_URL = 'https://aviapages.com/sitemap.xml'

logging.basicConfig(level=logging.INFO)


def main():

    # Download main sitemap
    download_main_sitemap()

    # Running tests
    tester = Parser(SITEMAP_PATH, int(os.environ.get('RETRIES_COUNT')), False)
    tester.run_test()


def download_main_sitemap() -> None:

    logger = logging.getLogger('DOWNLOADER')
    logger.info('Downloading sitemap file...')

    headers = parser.generate_headers()
    request = requests.get(MAIN_SITEMAP_URL, headers=headers)
    with open(SITEMAP_PATH, 'w') as file:
        file.write(request.text)

    logger.info(f'Sitemap file downloaded at {SITEMAP_PATH}')


if __name__ == '__main__':
    main()
