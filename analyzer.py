import csv
import logging
import os
from pathlib import Path
import re
import ssl

import parser

import contractions
import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar
from redis import Redis

import nltk

BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)

MIN_WORDS_COUNT = os.environ.get('MIN_WORDS_COUNT')


def analyze(all_links: set) -> None:

    download_nltk_data()

    logger = logging.getLogger('SEO ANALYZER')
    logger.info('Start of analyzing headers and article bodies...')

    redis = Redis('localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

    with alive_bar(len(all_links)) as bar:
        for link in all_links:

            headers = parser.generate_headers()
            request = requests.get(link, headers=headers)
            soup = BeautifulSoup(request.text, features='lxml-xml')

            # TITLE
            title = soup.find('h1', class_='thread_text ap_fs_24')
            if title:
                title_text = title.text.strip().upper()
            word_list = get_words_list(title_text)
            for word in word_list:
                redis.zincrby('headers', 1, word)

            # ARTICLE BODY
            article_body = ''
            body_p = soup.find('div', class_='message ap_margin_top_20').findAll('p')
            for p in body_p:
                article_body += p.text.strip() + ' '
            article_body = article_body.strip().upper()
            word_list = get_words_list(article_body)
            for word in word_list:
                redis.zincrby('article_bodies', 1, word)

            # Progress bar
            bar()

    # Generating reports
    logger.info('Start of generating reports...')

    # TITLE
    with open('/temp/seo_headers.csv', 'w', encoding='UTF8') as file:
        writer = csv.writer(file)

        # HEADERS
        report_headers = ['WORD', 'COUNT']
        writer.writerow(report_headers)

        # ROWS
        all_words = redis.zrangebyscore('headers', MIN_WORDS_COUNT, '+inf', withscores=True)
        all_words.reverse()
        for item in all_words:
            writer.writerow([item[0], int(item[1])])
    logger.info(f'Report file created at {BASE_DIR}/seo_headers.csv')

    # ARTICLE BODY
    with open('/temp/seo_bodies.csv', 'w', encoding='UTF8') as file:
        writer = csv.writer(file)

        # HEADERS
        report_headers = ['WORD', 'COUNT']
        writer.writerow(report_headers)

        # ROWS
        all_words = redis.zrangebyscore('article_bodies', MIN_WORDS_COUNT, '+inf', withscores=True)
        all_words.reverse()
        for item in all_words:
            writer.writerow([item[0], int(item[1])])
    logger.info(f'Report file created at {BASE_DIR}/seo_bodies.csv')

    # Clearing DB and cache
    redis.flushall()
    # Closing connection
    redis.close()


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

    # Final processing
    stop_words = nltk.corpus.stopwords.words('english')
    for word in words:
        if not word.isdigit() and len(word) > 1 and word not in stop_words:
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

    nltk_data = ['punkt', 'wordnet', 'omw-1.4', 'stopwords']
    with alive_bar(len(nltk_data)) as bar:
        for name in nltk_data:
            nltk.download(name, quiet=True)
            # Progress bar
            bar()
