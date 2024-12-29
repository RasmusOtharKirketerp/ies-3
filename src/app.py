from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pipeline_helper import run_pipeline, step_3_score_articles
from datetime import datetime
from scoring_words import ScoringWords

app = Flask(__name__)

scoring_words = ScoringWords()

def get_articles(db_path='articles.db', limit=10):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT title, rewrite_text, top_image, url, base_url, score, publish_date FROM articles WHERE rewrite_text > '' ORDER BY score DESC LIMIT ?""", (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_todays_articles(db_path='articles.db', limit=10):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT title, rewrite_text, top_image, url, base_url, score, publish_date FROM articles WHERE rewrite_text > '' AND date(publish_date) = date(?) ORDER BY score DESC LIMIT ?""", (today, limit))
    articles = cursor.fetchall()
    conn.close()

    return articles

def get_original_articles(db_path='articles.db', limit=10):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, text, top_image, url, base_url, score, publish_date 
        FROM articles 
        WHERE text > '' 
        ORDER BY score DESC 
        LIMIT ?""", (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_negative_scored_articles(db_path='articles.db', limit=100):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, text, top_image, url, base_url, score, publish_date 
        FROM articles 
        WHERE score < 1 
        ORDER BY score DESC 
        LIMIT ?""", (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_google_favicon(url):
    return f"https://www.google.com/s2/favicons?domain={url}"

@app.route('/recalculate-scores', methods=['POST'])
def recalculate_scores():
    try:
        recalculate_all_scores()
        return 'Success', 200
    except Exception as e:
        print(f"Error during recalculation: {e}")
        return 'Error', 500

def recalculate_all_scores():
    from score_text import score_articles_in_db
    score_articles_in_db(rescoring=True)

@app.route('/')
def index():
    articles = get_articles(limit=100)
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon)

@app.route('/today')
def today():
    articles = get_todays_articles(limit=100)
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon)

@app.route('/original')
def original():
    articles = get_original_articles(limit=100)
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon)

@app.route('/negative')
def negative():
    articles = get_negative_scored_articles()
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon)

@app.route('/words')
def words():
    all_words = scoring_words.get_all_user_words()
    return render_template('words.html', words=all_words)

@app.route('/words/add', methods=['POST'])
def add_word():
    word_da = request.form.get('word_da')
    word_en = request.form.get('word_en')
    weight = float(request.form.get('weight', 0.0))
    scoring_words.add_word(word_da, word_en, weight, 'user-word')
    recalculate_all_scores()
    return redirect(url_for('words'))

@app.route('/words/delete', methods=['POST'])
def delete_word():
    word_da = request.form.get('word_da')
    word_en = request.form.get('word_en')
    scoring_words.delete_word(word_da, word_en)
    recalculate_all_scores()
    return redirect(url_for('words'))

@app.route('/words/update', methods=['POST'])
def update_word():
    word_da = request.form.get('word_da')
    word_en = request.form.get('word_en')
    new_weight = float(request.form.get('new_weight', 0.0))
    scoring_words.update_weight(word_da, word_en, new_weight)
    recalculate_all_scores()
    return redirect(url_for('words'))

def start_flask():
    """Start the Flask app."""
    app.run(debug=True, use_reloader=True)


if __name__ == '__main__':
    
    # Start the Flask app
    start_flask()
