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


