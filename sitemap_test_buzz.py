import os
from pathlib import Path

from parser import Parser
from analyzer import Analyzer

BASE_DIR = Path(__file__).resolve().parent
SITEMAP_PATH = f'{BASE_DIR}/sitemaps/buzz_sitemap.xml'


def main():

    # Running tests
    tester = Parser(SITEMAP_PATH, int(os.environ.get('RETRIES_COUNT')), True)
    tester.run_test()

    # Running SEO analyze
    if int(os.environ.get('ANALYZE_SEO_BUZZ')) == 1:
        analyzer = Analyzer(SITEMAP_PATH)
        analyzer.analyze()


if __name__ == '__main__':
    main()
