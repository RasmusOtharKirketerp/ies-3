import sqlite3

def drop_table_article (db_path='articles.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS articles
    ''')
    
    conn.commit()
    conn.close()

def prepare_db(db_path='articles.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_url TEXT NOT NULL,
            url TEXT UNIQUE,
            title TEXT  DEFAULT NULL,
            authors TEXT DEFAULT NULL,
            publish_date TEXT ,
            text TEXT DEFAULT NULL,
            top_image TEXT,
            score INTEGER DEFAULT 0,
            rewrite_text TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()
    return conn

def delete_all_articles(db_path='articles.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM articles
    ''')
    conn.commit()
    conn.close()

def store_urls(base_url, urls, db_path='articles.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for url in urls:
        print(f"Storing {url}")
        cursor.execute('''
            INSERT OR IGNORE INTO articles (base_url, url) VALUES (?, ?)
        ''', (base_url, url,))
    conn.commit()
    conn.close()

def update_article(article_data, db_path='articles.db'):
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


def store_article(base_url, article_data, db_path='articles.db'):
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
    drop_table_article()
    prepare_db()
    article_data = {
        'url': 'https://nyheder.tv2.dk/samfund/2024-12-24-familie-var-centimeter-fra-at-blive-paakoert-det-var-helt-sindssygt',
        'title': 'Familie var centimeter fra at blive påkørt: Det var helt sindssygt',
        'authors': ['Mads Gudiksen'],
        'publish_date': None,
        'text': 'En familie på fire slap med skrækken, da en bilist i høj fart kørte ind i deres have.',
        'top_image': 'https://tv2.dk/image/5f9a7c0d5d5f3c1f6c000001.jpg?preset=article-image'
    }
    store_article('https://nyheder.tv2.dk', article_data)