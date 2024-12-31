# this file discovers the main page of the website and saves only the urls of the articles in the db
import discover_articles
from pipeline_helper import fetch_urls_for_download
from save_raw_article import prepare_db, store_urls, update_article
from downloan_articles import download_article
from score_text import score_articles_in_db
import os

if __name__ == '__main__':
    #delete the db file if it exists
    DB_PATH = 'test_articles.db'
    #os.remove(DB_PATH)
    prepare_db(DB_PATH)
    base_url = 'https://nyheder.tv2.dk/'
    urls = discover_articles.discover_articles(base_url)
    print(urls)
    store_urls(base_url, urls,DB_PATH)
    print('urls saved')

    dl = fetch_urls_for_download(DB_PATH)
    #loop the 10 first urls and download the articles

    for url in dl[:10]:
        print(f'Downloading article: {url}')
        article_data = download_article(url, retries=3, delay=10, db_path=DB_PATH)
        print(f'Storing article: {url}')
        #save_raw_article.store_article(base_url, article_data)
        update_article(article_data, DB_PATH)

    score_articles_in_db(DB_PATH)

