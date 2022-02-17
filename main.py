import parser

SITEMAP_LINK = 'https://aviapages.com/sitemap.xml'
RETRIES_COUNT = 3


def main():

    # Getting all links from the sitemap
    all_links = parser.parse_sitemap(SITEMAP_LINK)

    # Running tests
    parser.run_test(all_links, RETRIES_COUNT)


if __name__ == '__main__':
    main()
