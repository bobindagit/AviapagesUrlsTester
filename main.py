import os
import parser


def main():

    # Getting all links from the sitemap
    all_links = parser.parse_sitemap(os.environ.get('SITEMAP_LINK'))

    # Running tests
    parser.run_test(all_links, int(os.environ.get('RETRIES_COUNT')))


if __name__ == '__main__':
    main()
