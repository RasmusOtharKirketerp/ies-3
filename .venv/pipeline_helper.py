#here is utility functions for the pipeline
import sqlite3

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

# website to be scraped and the time to wait between each discovery and downloan request in minutes
websites = {
    'https://nyheder.tv2.dk/': 60,  
    'https://www.dr.dk/nyheder/': 60, 
    'https://www.bt.dk/': 60,  
    'https://ekstrabladet.dk/': 60,
    'https://www.berlingske.dk/': 60,
    'https://www.version2.dk/': 60  
}

### step 1 - discover_articles
def step_1_deamon_discover_articles(base_url):
    #this function discovers the main page of the website and saves only the urls of the articles in the db
    import discover_articles
    from pipeline_helper import fetch_urls_for_download
    from save_raw_article import prepare_db, store_urls, update_article
    from downloan_articles import download_article
    from score_text import score_articles_in_db

    urls = discover_articles.discover_articles(base_url)
    store_urls(base_url, urls)

def run_step_1_as_deamon():
    import time
    import threading
    for base_url in websites.keys():
        threading.Thread(target=step_1_deamon_discover_articles, args=(base_url,)).start()
    while True:
        print('Discover articles deamon sleeping')
        time.sleep(websites[base_url]*60)

### step 2 - download_articles
def step_2_deamon_download_articles():
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
    
def run_step_2_as_deamon():
    import time
    import threading
    threading.Thread(target=step_2_deamon_download_articles).start()
    while True:
        print('Download articles deamon sleeping')
        time.sleep(60)
        
### step 3 - score_articles
def step_3_deamon_score_articles():
    #this function scores the articles in the db
    from score_text import score_articles_in_db
    print('Scoring articles')
    score_articles_in_db()

def run_step_3_as_deamon():
    import time
    import threading
    threading.Thread(target=step_3_deamon_score_articles).start()
    while True:
        print('Scoring articles deamon sleeping')
        time.sleep(30)

### step 4 - rewrite_articles
def step_4_deamon_rewrite_articles():
    #this function rewrites the articles in the db
    from ollama_rewrite_main import rewrite_text_in_db
    print('Rewriting articles')
    rewrite_text_in_db()

def run_step_4_as_deamon():
    import time
    import threading
    threading.Thread(target=step_4_deamon_rewrite_articles).start()
    while True:
        print('Rewriting articles deamon sleeping')
        time.sleep(60)

def run_pipeline():   
    import threading
    threading.Thread(target=run_step_1_as_deamon).start()
    threading.Thread(target=run_step_2_as_deamon).start()
    threading.Thread(target=run_step_3_as_deamon).start()
    threading.Thread(target=run_step_4_as_deamon).start()

if __name__ == '__main__':
    run_pipeline()



















################################################################################################
# utility functions for the pipeline
################################################################################################
def fetch_urls_for_download(db_path='articles.db'):
    #this function fetches the urls of the articles to be downloaded
    #from the database where there are no titles or text
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT url FROM articles WHERE title IS NULL
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


