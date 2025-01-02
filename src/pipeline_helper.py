#here is utility functions for the pipeline
import sqlite3
import time
from datetime import datetime
from score_text import score_articles_in_db
from scoring_words import ScoringWords
import db_layer
from download_articles import download_article



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
def get_active_websites(DB_PATH):
    sw = ScoringWords(DB_PATH)
    websites = {}
    for url, refresh_time, language, active in sw.get_all_websites():
        if active:
            websites[url] = refresh_time
    return websites

### step 1 - discover_articles
def step_1_discover_articles(base_url):
    #this function discovers the main page of the website and saves only the urls of the articles in the db
    import discover_articles
    

    urls = discover_articles.discover_articles(base_url)
    db_layer.store_urls(base_url, urls, DB_PATH)

### step 2 - download_articles
def step_2_download_articles(DB_PATH):
    #this function downloads the articles from the urls in the db

    dl = db_layer.fetch_urls_for_download(DB_PATH)
    for url in dl:
        print(f'Downloading article: {url}')
        article_data = download_article(url, retries=3, delay=10, db_path=DB_PATH)
        if article_data['title'] == "Download failed":
            print(f"Skipping article {url} due to download failure.")
            continue
        print(f'Updating article: {url}')
        db_layer.update_article(article_data, DB_PATH)

### step 3 - score_articles
def step_3_score_articles(DB_PATH):
    #this function scores the articles in the db
    print('Scoring articles')
    score_articles_in_db(DB_PATH)


### step 4 - rewrite_articles
def step_4_deamon_rewrite_articles(DB_PATH):
    #this function rewrites the articles in the db
    from rewrite_nlp import rewrite_all_nlp
    print('Rewriting articles')
    rewrite_all_nlp()

def copy_articles_from_share_to_user(DB_PATH):
    # make sure that user has no articles
    db_layer.delete_all_articles(DB_PATH)

    # this function copies the articles from the SHARE user to the user
    user_websites = db_layer.get_users_websites(DB_PATH)
    
    share_articles = db_layer.get_all_articles_from_share()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for article in share_articles:
        if article[6] in user_websites:  # base_url is the 7th element in the tuple
            cursor.execute('''
                INSERT INTO articles (url, title, authors, publish_date, text, top_image, base_url, score, rewrite_text) VALUES (?,?,?,?,?,?,?,?,?)
            ''', article)
    conn.commit()
    conn.close()

def run_pipeline(DB_PATH, user_id):
    # Prepare the database
    db_layer.prepare_db(DB_PATH)
    
    while True:
        if user_id == 'SHARE':
            websites = get_active_websites(DB_PATH)
            for base_url, wait_time in websites.items():
                print(f'Discovering articles for {base_url}')
                step_1_discover_articles(base_url)
            step_2_download_articles(DB_PATH)
        if user_id != 'SHARE':
            copy_articles_from_share_to_user(DB_PATH)
        if user_id == 'SHARE':
            print('Skipping scoring for SHARE user')
        if user_id != 'SHARE':
            step_3_score_articles(DB_PATH)
        if user_id == 'SHARE':
            step_4_deamon_rewrite_articles(DB_PATH)
        wait_time = 60
        print("Datetime: ", datetime.now())
        print(f'Waiting {wait_time} seconds')
        time.sleep(wait_time)
    

if __name__ == '__main__':
    # get database path from start parameters
    import sys
    if len(sys.argv) < 1:
        print("Usage: python pipeline_helper <db_path> <user_id>")
        sys.exit(1)
    DB_PATH = sys.argv[1]
    user_id = sys.argv[2]
    print(f"Starting app with db_path={DB_PATH}")
    db_layer.prepare_db(DB_PATH)
    # Initialize websites if running for the first time
    sw = ScoringWords(DB_PATH)
    if not sw.get_all_websites():
        sw.populate_sample_websites()
    run_pipeline(DB_PATH, user_id)
