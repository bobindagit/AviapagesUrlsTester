import os
from pathlib import Path
import logging
import parser
import analyzer

BASE_DIR = Path(__file__).resolve().parent
SITEMAP_PATH = f'{BASE_DIR}/sitemaps/buzz_sitemap.xml'

logging.basicConfig(level=logging.INFO)


def main():

    # Getting all links from the sitemap
    all_links = parser.get_sitemap_links(SITEMAP_PATH)

    # Running tests
    parser.run_test(all_links,
                    int(os.environ.get('RETRIES_COUNT')),
                    True)

    # Running SEO analyze
    if int(os.environ.get('ANALYZE_SEO_BUZZ')) == 1:
        analyzer.analyze(all_links)


if __name__ == '__main__':
    main()
