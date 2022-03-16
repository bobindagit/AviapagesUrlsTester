import csv
import os.path
import time
import logging
from pathlib import Path

import asyncio
import aiohttp
import concurrent.futures

from alive_progress import alive_it, alive_bar
from random_user_agent.user_agent import UserAgent
from bs4 import BeautifulSoup

BASE_URL = 'http://aviapages.com'
BASE_DIR = Path(__file__).resolve().parent

NUM_CORES = int(os.environ.get('NUM_CORES'))

logging.basicConfig(level=logging.INFO)


class Parser:
    def __init__(self, sitemap_path: str, retries_count: int, test_buzz: bool):
        self.sitemap_links = get_sitemap_links(sitemap_path)
        self.retries_count = retries_count
        self.test_buzz = test_buzz
        reports_path = f'{BASE_DIR}/reports'
        if not os.path.exists(reports_path):
            os.mkdir(reports_path)
        self.filename = f'{reports_path}/report_buzz.csv' if test_buzz else f'{reports_path}/report_main.csv'

    def run_test(self) -> None:

        logger = logging.getLogger('TESTER')
        logger.info('Testing site urls...')

        # HEADERS
        with open(self.filename, 'w', encoding='UTF8') as file:
            writer = csv.writer(file)

            retries_headers = []
            for i in range(1, self.retries_count + 1):
                retries_headers.append(f'RETRY_{i}')
            report_headers = ['URL'] + retries_headers + ['AVERAGE_TIME', 'RESPONSE']
            if self.test_buzz:
                report_headers += ['IMAGE_SIZE']
            writer.writerow(report_headers)

        # ROWS
        with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
            with alive_bar(total=len(self.sitemap_links)) as bar:
                futures = []
                for link in self.sitemap_links:
                    future = executor.submit(self.test_link, link)
                    future.add_done_callback(lambda p: bar())
                    futures.append(future)
                results = []
                for future in futures:
                    result = future.result()
                    results.append(result)

        logger.info(f'Report file created at {self.filename}')

    def test_link(self, link: str) -> None:

        with open(self.filename, 'a+', encoding='UTF8') as file:
            status_code = 0
            elapsed_time = 0
            if self.test_buzz:
                image_size = 0

            # Link
            row = [link]

            links_info = asyncio.run(self.get_link_detailed_info(link))
            for link_info in links_info:
                # Elapsed time
                row.append("{:.5f}".format(link_info.get('elapsed_time')))

                elapsed_time += link_info.get('elapsed_time')

                response_code = link_info.get('response')
                if status_code == 0 or response_code != 200:
                    status_code = response_code

                # Only for buzz, only if image wasn't parsed
                if self.test_buzz and response_code == 200 and image_size == 0:
                    current_image_size = link_info.get('image_size')
                    if current_image_size != 0:
                        image_size = current_image_size

            # Average elapsed time
            row.append("{:.5f}".format(elapsed_time / self.retries_count))

            # Response code
            row.append(status_code)

            # Image size (only for buzz)
            if self.test_buzz:
                row.append(image_size)

            # Row write
            writer = csv.writer(file)
            writer.writerow(row)

    async def get_link_detailed_info(self, link: str) -> list:

        async with aiohttp.ClientSession(headers=generate_headers(), trust_env=True) as session:
            tasks = []
            for i in range(1, self.retries_count + 1):
                tasks.append(asyncio.ensure_future(self.get_link_info(session, link)))

            return await asyncio.gather(*tasks)

    async def get_link_info(self, session, link: str) -> dict:

        start_time = time.time()
        async with session.get(link) as request:
            elapsed_time = (time.time() - start_time) * 1000
            response = request.status

            # Parsing main image only for buzz mode
            if self.test_buzz and response == 200:
                request_text = await request.text()
                image_size = await self.get_image_size(session, request_text)
            else:
                image_size = 0

            return {
                'elapsed_time': elapsed_time,
                'response': response,
                'image_size': image_size
            }

    @staticmethod
    async def get_image_size(session, link_content: str) -> str:

        soup = BeautifulSoup(link_content, features='lxml-xml')
        image = soup.find('img', class_='thread_image')
        if image:
            image_url = BASE_URL + image.get('src')
            async with session.get(image_url) as image_request:
                if image_request.status == 200:
                    return "{:.5f}".format(image_request.content_length / 1024)

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


def get_sitemap_links(sitemap_path: str) -> set:

    logger = logging.getLogger('LINKS PARSER')
    logger.info('Reading sitemap file...')

    links = set()
    with open(sitemap_path, 'r') as file:
        soup = BeautifulSoup(file.read(), features="lxml-xml")

        link_tags = soup.find_all("loc")
        for link_tag in alive_it(link_tags):
            links.add(link_tag.text)

    return links
