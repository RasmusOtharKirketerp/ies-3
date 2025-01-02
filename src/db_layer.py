#db layer for the articles 
import sqlite3


#support for the pipeline
#####################################
def fetch_urls_for_download(db_path):
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

def update_rewrite_text_by_id(article_id, rewritten_text, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE articles SET rewrite_text=? WHERE id=?
    ''', (rewritten_text, article_id))
    conn.commit()
    conn.close()

def store_urls(base_url, urls, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for url in urls:
        # Check if the base_url is in the string of url
        if base_url not in url:
            print(f"URL {url} does not contain the base URL {base_url}, skipping")
            continue

        
        if chech_if_raw_url_is_db(url, db_path):
            print(f"URL {url} already in database, skipping")
            continue
        cursor.execute('''
            INSERT OR IGNORE INTO articles (base_url, url) VALUES (?, ?)
        ''', (base_url, url,))
    conn.commit()
    conn.close()

def get_users_websites(DB_PATH):
    # this function fetches the websites of the user
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT url FROM websites''')
    websites = cursor.fetchall()
    conn.close()
    return [website[0] for website in websites]


def store_article(base_url, article_data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO articles (
            base_url, url, title, authors, publish_date, text, top_image
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        base_url,
        article_data['url'],
        article_data['title'],
        ', '.join(article_data['authors']),
        article_data['publish_date'].strftime('%Y-%m-%d') if article_data['publish_date'] else None,
        article_data['text'],
        article_data['top_image']
    ))
    conn.commit()
    conn.close()


def update_article(article_data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE articles SET title=?, authors=?, publish_date=?, text=?, top_image=? WHERE url=?
    ''', (
        article_data['title'],
        ', '.join(article_data['authors']),
        article_data['publish_date'].strftime('%Y-%m-%d') if article_data['publish_date'] else None,
        article_data['text'],
        article_data['top_image'],
        article_data['url']
    ))
    conn.commit()
    conn.close()


def chech_if_url_need_download(url, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT url FROM articles WHERE url=? and title = ''
    ''', (url,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    else:
        return True
    
def fetch_urls_for_download(db_path):
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
    
def fecth_article_txt_by_id(article_id, db_path):
    #this function fetches the text of the article by the id
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT text FROM articles WHERE id=?
    ''', (article_id,))
    text = cursor.fetchone()[0]
    conn.close()
    return text
    
def chech_if_raw_url_is_db(url, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT url FROM articles WHERE url=?
    ''', (url,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    else:
        return True
    
def fetch_id_and_text_from_articles(db_path):
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
    
def get_website_language(url, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM websites WHERE ? LIKE "%" || url || "%"', (url,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'da'  # default to Danish if not found
    
def get_cached_articles(url, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT url, title, authors, publish_date, text, top_image FROM articles WHERE url=? LIMIT 1
    ''', (url,))
    article = cursor.fetchone()
    conn.close()
    if not article:
        return None
    else:
        return {
            'url': article[0],
            'title': article[1],
            'authors': article[2].split(', ') if article[2] else [],
            'publish_date': article[3],
            'text': article[4],
            'top_image': article[5]
        }
    
def get_all_articles_from_share():
    # this function fetches all the articles from the SHARE user
    conn = sqlite3.connect("share_articles.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT url, title, authors, publish_date, text, top_image, base_url, score, rewrite_text FROM articles''')
    articles = cursor.fetchall()
    conn.close()
    return articles

def fecth_all_id_and_text_and_base_url(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, text, base_url FROM articles WHERE score IS NULL')
    
    articles = cursor.fetchall()
    conn.close()
    return articles

def update_score_by_id(article_id, score, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE articles SET score=? WHERE id=?
    ''', (score, article_id))
    conn.commit()
    conn.close()

def redownload_all_articles(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE articles SET title=NULL, authors=NULL, publish_date=NULL, text=NULL, top_image=NULL, score=NULL, rewrite_text=NULL
    ''')
    conn.commit()
    conn.close()
 

def fetch_id_and_text_from_articles_with_no_score(db_path):
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


# General DB functions
def fetch_all_articles(db_path):
    #this function fetches all articles from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, url, title, authors, publish_date, text, top_image, base_url FROM articles
    ''')
    articles = cursor.fetchall()
    conn.close()
    return articles

def delete_all_articles(DB_PATH):
    # this function deletes all the articles from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM articles
    ''')
    conn.commit()
    conn.close()


def drop_table_article (db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS articles
    ''')
    
    conn.commit()
    conn.close()

# Prepare the database
#####################################
def prepare_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            title TEXT,
            authors TEXT,
            publish_date TEXT,
            text TEXT,
            top_image TEXT,
            base_url TEXT,
            score REAL,
            rewrite_text TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            refresh_time INTEGER NOT NULL,
            language TEXT NOT NULL,
            active BOOLEAN DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

# SQL for testing
def TEST_get_10_articles_with_text(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, url, title, authors, publish_date, text, top_image, base_url FROM articles WHERE text > ' ' LIMIT 10
    ''')
    articles = cursor.fetchall()
    conn.close()
    return articles

