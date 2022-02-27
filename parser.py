import csv
import requests
import logging
from pathlib import Path
from alive_progress import alive_it
from random_user_agent.user_agent import UserAgent
from bs4 import BeautifulSoup

BASE_URL = 'http://aviapages.com'
BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)


def get_sitemap_links(sitemap_path: str) -> set:

    logger = logging.getLogger('LINKS PARSER')
    logger.info('Reading SITEMAP file...')

    links = set()
    with open(sitemap_path, 'r') as file:
        soup = BeautifulSoup(file.read(), features="lxml-xml")

        link_tags = soup.find_all("loc")
        for link_tag in alive_it(link_tags):
            links.add(link_tag.text)

    return links


def run_test(links: set, retries_count: int, test_buzz: bool) -> None:

    logger = logging.getLogger('TESTER')
    logger.info('Start of testing...')

    filename = 'report_buzz.csv' if test_buzz else 'report_main.csv'

    with open(filename, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)

        # HEADERS
        retries_headers = []
        for i in range(1, retries_count + 1):
            retries_headers.append(f'RETRY_{i}')
        report_headers = ['URL'] + retries_headers + ['AVERAGE_TIME', 'RESPONSE']
        if test_buzz:
            report_headers += ['IMAGE_SIZE']
        writer.writerow(report_headers)

        # ROWS
        for link in alive_it(links):

            status_code = 0
            elapsed_time = 0
            if test_buzz:
                image_size = 0

            # Link
            row = [link]

            for i in range(1, retries_count + 1):
                link_info = test_link_connection(link, test_buzz)
                # Elapsed time
                row.append("{:.5f}".format(link_info.get('elapsed_time')))

                elapsed_time += link_info.get('elapsed_time')

                response_code = link_info.get('response')
                if status_code == 0 or response_code != 200:
                    status_code = response_code

                # Only for buzz, only if image wasn't parsed
                if test_buzz and response_code == 200 and image_size == 0:
                    current_image_size = link_info.get('image_size')
                    if current_image_size != 0:
                        image_size = current_image_size

            # Average elapsed time
            row.append("{:.5f}".format(elapsed_time / retries_count))

            # Response code
            row.append(status_code)

            # Image size (only for buzz)
            if test_buzz:
                row.append(image_size)

            writer.writerow(row)

    logger.info(f'Report file created at {BASE_DIR}/{filename}')


def test_link_connection(link: str, test_buzz: bool) -> dict:

    headers = generate_headers()

    request = requests.get(link, headers=headers)

    elapsed_time = request.elapsed.total_seconds() * 1000
    response = request.status_code

    # Parsing main image only for buzz mode
    if test_buzz and response == 200:
        image_size = get_image_size(request.text, headers)
    else:
        image_size = 0

    return {
        'elapsed_time': elapsed_time,
        'response': response,
        'image_size': image_size
    }


def get_image_size(link_content: str, headers: dict) -> str:

    soup = BeautifulSoup(link_content, features='lxml-xml')
    image = soup.find('img', class_='thread_image')
    if image:
        image_url = BASE_URL + image.get('src')
        image_request = requests.get(image_url, headers=headers)
        if image_request.status_code == 200:
            return "{:.5f}".format(len(image_request.content) / 1024)

    return 0


def generate_headers() -> dict:
    user_agent_rotator = UserAgent()
    return {
        'User-Agent': user_agent_rotator.get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1"
    }
