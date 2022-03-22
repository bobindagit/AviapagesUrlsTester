import os
import logging
import csv
from pathlib import Path
import ssl
from redis import Redis

from alive_progress import alive_it

from bs4 import BeautifulSoup

import re
import contractions
import nltk

import asyncio
import aiohttp
import aioredis

import parser

BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)


class Analyzer:
    def __init__(self, sitemap_path: str):
        self.sitemap_links = parser.get_sitemap_links(sitemap_path)
        self.min_words_count = os.environ.get('MIN_WORDS_COUNT')
        self.logger = logging.getLogger('SEO ANALYZER')

    def analyze(self) -> None:

        reports_path = f'{BASE_DIR}/reports'
        if not os.path.exists(reports_path):
            os.mkdir(reports_path)

        # Service NLTK data
        download_nltk_data()

        # Parsing header and body words
        self.logger.info('Start of analyzing headers and article bodies...')

        async_redis = aioredis.from_url(url='redis://localhost', port=6379, db=0, encoding='utf-8',
                                        decode_responses=True)
        asyncio.run(self.parse_links(async_redis))

        # Generating reports
        self.logger.info('Start of generating reports...')

        redis = Redis.from_url(url='redis://localhost', port=6379, db=0, encoding='utf-8', decode_responses=True)

        # TITLE
        with open(f'{reports_path}/seo_headers.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)

            # HEADERS
            report_headers = ['WORD', 'COUNT']
            writer.writerow(report_headers)

            # ROWS
            all_words = redis.zrangebyscore('headers', self.min_words_count, '+inf', withscores=True)
            all_words.reverse()
            for item in all_words:
                writer.writerow([item[0], int(item[1])])
        self.logger.info(f'Report file created at {reports_path}/seo_headers.csv')

        # ARTICLE BODY
        with open(f'{reports_path}/seo_bodies.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)

            # HEADERS
            report_headers = ['WORD', 'COUNT']
            writer.writerow(report_headers)

            # ROWS
            all_words = redis.zrangebyscore('article_bodies', self.min_words_count, '+inf', withscores=True)
            all_words.reverse()
            for item in all_words:
                writer.writerow([item[0], int(item[1])])
        self.logger.info(f'Report file created at {reports_path}/seo_bodies.csv')

        # Clearing DB and cache
        redis.flushall()
        # Closing connection
        redis.close()

    async def parse_links(self, redis) -> None:
        async with aiohttp.ClientSession(headers=parser.generate_headers(), trust_env=True) as session:
            tasks = []
            for link in alive_it(self.sitemap_links):
                tasks.append(asyncio.ensure_future(self.parse_words(session, redis, link)))

            await asyncio.gather(*tasks)
            await redis.save()
            await redis.close()

    async def parse_words(self, session, redis, link: str) -> None:
        try:
            async with session.get(link) as request:
                request_text = await request.text()
                soup = BeautifulSoup(request_text, features='lxml-xml')

                # TITLE
                title = soup.find('h1', class_='thread_text ap_fs_24')
                if title:
                    title_text = title.text.strip().upper()
                    word_list = get_words_list(title_text)
                    for word in word_list:
                        await redis.zincrby('headers', 1, word)

                # ARTICLE BODY
                article_body = ''
                body = soup.find('div', class_='message ap_margin_top_20')
                if body:
                    for p in body.findAll('p'):
                        article_body += p.text.strip() + ' '
                    article_body = article_body.strip().upper()
                    word_list = get_words_list(article_body)
                    for word in word_list:
                        await redis.zincrby('article_bodies', 1, word)
        except asyncio.TimeoutError:
            self.logger.error(f'Timeout error at {link}')


def get_words_list(text: str) -> list:
    # Punctuation remover
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

    # Removing URLS
    words = re.sub(r'http\S+', '', text)

    # CONTRACTION fix
    words = contractions.fix(words)

    # Lemmatizer
    lemmatizer = nltk.WordNetLemmatizer()

    # Tokenizing text
    words = tokenizer.tokenize(words)

    # Word list for return
    word_list = []

    # Useless words
    stop_words = nltk.corpus.stopwords.words('english')

    for word in words:
        if not word.isdigit() and len(word) > 1 and word.lower() not in stop_words:
            # Lemmatizing verb
            word = lemmatizer.lemmatize(word)
            word = lemmatizer.lemmatize(word, pos='v')

            word_list.append(word)

    return word_list


def download_nltk_data() -> None:
    logger = logging.getLogger('SERVICE')
    logger.info('Downloading service data...')

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk_data = ('punkt', 'wordnet', 'omw-1.4', 'stopwords')
    for name in alive_it(nltk_data):
        nltk.download(name, quiet=True)
