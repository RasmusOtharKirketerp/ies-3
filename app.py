from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_articles(db_path='articles.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT title, rewrite_text, top_image, url, base_url FROM articles where rewrite_text > '' order by score desc""")
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_google_favicon(url):
    return f"https://www.google.com/s2/favicons?domain={url}"

@app.route('/')
def index():
    articles = get_articles()
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon)

if __name__ == '__main__':
    app.run(debug=True)
