import sqlite3

def drop_table_article (db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS articles
    ''')
    
    conn.commit()
    conn.close()

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

def delete_all_articles(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM articles
    ''')
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

if __name__ == '__main__':
    db_path = 'test_articles.db'
    prepare_db(db_path= db_path)
    article_data = {
        'url': 'https://nyheder.tv2.dk/samfund/2024-12-24-familie-var-centimeter-fra-at-blive-paakoert-det-var-helt-sindssygt',
        'title': 'Familie var centimeter fra at blive påkørt: Det var helt sindssygt',
        'authors': ['Mads Gudiksen'],
        'publish_date': None,
        'text': 'En familie på fire slap med skrækken, da en bilist i høj fart kørte ind i deres have.',
        'top_image': 'https://tv2.dk/image/5f9a7c0d5d5f3c1f6c000001.jpg?preset=article-image'
    }
    store_article('https://nyheder.tv2.dk', article_data, db_path)