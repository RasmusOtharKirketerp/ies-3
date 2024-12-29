from flask import Flask, render_template
import sqlite3
import threading
import time
from pipeline_helper import run_pipeline

app = Flask(__name__)

def get_articles(db_path='articles.db', limit=10):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT title, rewrite_text, top_image, url, base_url FROM articles WHERE rewrite_text > '' ORDER BY publish_date desc,  score DESC LIMIT ?""", (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_google_favicon(url):
    return f"https://www.google.com/s2/favicons?domain={url}"

@app.route('/')
def index():
    articles = get_articles(limit=20)
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon)

def start_flask():
    """Start the Flask app."""
    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    
    # Start the Flask app
    start_flask()
