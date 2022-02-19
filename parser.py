import csv
import requests
import logging
from alive_progress import alive_it
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


def parse_sitemap(sitemap_link: str) -> set:

    logger = logging.getLogger('PARSER')

    # Links list
    links = set()

    fake_user = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': fake_user.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1"
    }

    logger.info('Getting SITEMAP file')
    request = requests.get(sitemap_link, headers=headers)
    soup = BeautifulSoup(request.text, features="lxml-xml")

    logger.info('Reading SITEMAP file')
    link_tags = soup.find_all("loc")
    for link_tag in alive_it(link_tags):
        links.add(link_tag.text)

    return links


def run_test(links: set, retries_count: int) -> None:

    logger = logging.getLogger('TESTER')

    with open('report.csv', 'w', encoding='UTF8') as file:
        writer = csv.writer(file)

        # HEADERS
        retries_headers = []
        for i in range(1, retries_count + 1):
            retries_headers.append(f'RETRY_{i}')
        report_headers = ['URL'] + retries_headers + ['AVERAGE_TIME', 'RESPONSE']
        writer.writerow(report_headers)

        logger.info('Start of testing')
        # ROWS
        for link in alive_it(links):

            status_code = 0
            elapsed_time = 0

            # Link
            row = [link]

            for i in range(1, retries_count + 1):
                link_info = test_link_connection(link)
                # Elapsed time
                row.append(link_info.get('elapsed_time'))

                elapsed_time += link_info.get('elapsed_time')

                response_code = link_info.get('response')
                if status_code == 0 or response_code != 200:
                    status_code = response_code

            # Average elapsed time
            row.append(elapsed_time / retries_count)

            # Response code
            row.append(status_code)

            writer.writerow(row)

    logger.info('Created file report.csv')


def test_link_connection(link: str) -> dict:

    fake_user = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': fake_user.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1"
    }

    request = requests.get(link, headers=headers)

    elapsed_time = request.elapsed.total_seconds()
    response = request.status_code

    return {
        'elapsed_time': elapsed_time,
        'response': response
    }
