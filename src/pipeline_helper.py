#here is utility functions for the pipeline
import sqlite3
import time
from datetime import datetime
from scoring_words import ScoringWords

# Decription of the pipeline
# ################################################################################################
# pipeline step 1 - discover_articles - discover the main page of the website and saves only the urls of the articles in the db
# pipeline step 2 - download_articles - download the articles from the urls in the db
# pipeline step 3 - score_articles - score the articles in the db
# pipeline step 4 - rewrite_articles - rewrite the articles in the db
# 
# pipelines will run independently and can be run in any order
# ################################################################################################
# each step will run as deamon and will be run in a loop with a sleep time

# Replace the websites dictionary
def get_active_websites():
    sw = ScoringWords()
    websites = {}
    for url, refresh_time, language, active in sw.get_all_websites():
        if active:
            websites[url] = refresh_time
    return websites

### step 1 - discover_articles
def step_1_discover_articles(base_url):
    #this function discovers the main page of the website and saves only the urls of the articles in the db
    import discover_articles
    from save_raw_article import store_urls

    urls = discover_articles.discover_articles(base_url)
    store_urls(base_url, urls)

### step 2 - download_articles
def step_2_download_articles():
    #this function downloads the articles from the urls in the db
    from pipeline_helper import fetch_urls_for_download
    from save_raw_article import update_article
    from downloan_articles import download_article

    dl = fetch_urls_for_download()
    for url in dl:
        print(f'Downloading article: {url}')
        article_data = download_article(url)
        print(f'Updating article: {url}')
        update_article(article_data)

### step 3 - score_articles
def step_3_score_articles():
    #this function scores the articles in the db
    from score_text import score_articles_in_db
    print('Scoring articles')
    score_articles_in_db()


### step 4 - rewrite_articles
def step_4_deamon_rewrite_articles():
    #this function rewrites the articles in the db
    from ollama_rewrite_main import rewrite_text_in_db
    print('Rewriting articles')
    rewrite_text_in_db()

def run_pipeline():
    while True:
        websites = get_active_websites()
        for base_url, wait_time in websites.items():
            print(f'Discovering articles for {base_url}')
            step_1_discover_articles(base_url)
        step_2_download_articles()
        step_3_score_articles()
        step_4_deamon_rewrite_articles()
        wait_time = 60
        print("Datetime: ", datetime.now())
        print(f'Waiting {wait_time} seconds')
        time.sleep(wait_time)
    

################################################################################################
# utility functions for the pipeline
################################################################################################
def fetch_urls_for_download(db_path='articles.db'):
    #this function fetches the urls of the articles to be downloaded
    #from the database where there are no titles or text
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT url FROM articles WHERE title IS NULL or title = '' 
    ''')
    urls = [row[0] for row in cursor.fetchall()]
    conn.close()
    return urls

def fecth_article_txt_by_id(article_id, db_path='articles.db'):
    #this function fetches the text of the article by the id
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT text FROM articles WHERE id=?
    ''', (article_id,))
    text = cursor.fetchone()[0]
    conn.close()
    return text

def fetch_id_and_text_from_articles(db_path='articles.db'):
    #this function fetches the id and text of the articles
    #from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, text FROM articles
    ''')
    articles = cursor.fetchall()
    conn.close()
    return articles

def fetch_id_and_text_from_articles_with_no_score(db_path='articles.db'):
    #this function fetches the id and text of the articles
    #from the database where the score is null
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, text FROM articles WHERE score IS NULL
    ''')
    articles = cursor.fetchall()
    conn.close()
    return articles


if __name__ == '__main__':
    # Initialize websites if running for the first time
    sw = ScoringWords()
    if not sw.get_all_websites():
        sw.populate_sample_websites()
    run_pipeline()
