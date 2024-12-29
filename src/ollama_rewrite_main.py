import sqlite3
import ollama_rewrite
from tqdm import tqdm

def fetch_id_and_text_from_articles(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, text FROM articles")
    articles = cursor.fetchall()

    conn.close()
    return articles

def fetch_id_and_text_from_articles_with_no_rewrite_text(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, text FROM articles WHERE text > '' and rewrite_text IS NULL")
    articles = cursor.fetchall()

    conn.close()
    return articles

def  rewrite_text_in_db(db_path='articles.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    articles = fetch_id_and_text_from_articles_with_no_rewrite_text(db_path)
    
    for article_id, text in tqdm(articles, desc="Processing articles for rewriting"):
        
        rewritten_text = ollama_rewrite.rewrite_text(text)
        cursor.execute('''
            UPDATE articles SET rewrite_text=? WHERE id=? 
        ''', (rewritten_text, article_id))
        #print(f"Rewritten article {article_id}")
        conn.commit()
    
    conn.close()
    
if __name__ == '__main__':
    rewrite_text_in_db()