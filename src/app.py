from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from db_layer import prepare_db
from datetime import datetime, timedelta
from scoring_words import ScoringWords
import os

app = Flask(__name__)

# Update all database functions to use DB_PATH
def get_articles(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT title, rewrite_text, top_image, url, base_url, score, publish_date FROM articles WHERE rewrite_text > '' ORDER BY score DESC LIMIT ?""", (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_todays_articles(limit=10):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT title, rewrite_text, top_image, url, base_url, score, publish_date FROM articles WHERE rewrite_text > '' AND date(publish_date) = date(?) ORDER BY score DESC LIMIT ?""", (today, limit))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_original_articles(limit=10):
    conn = sqlite3.connect(DB_PATH)
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

def get_negative_scored_articles(limit=100):
    conn = sqlite3.connect(DB_PATH)
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
    score_articles_in_db(DB_PATH)

@app.route('/')
def index():
    articles = get_articles(limit=100)
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon, user_id=USER_ID)

@app.route('/today')
def today():
    articles = get_todays_articles(limit=100)
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon, user_id=USER_ID)

@app.route('/original')
def original():
    articles = get_original_articles(limit=100)
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon, user_id=USER_ID)

@app.route('/negative')
def negative():
    articles = get_negative_scored_articles()
    return render_template('index.html', articles=articles, get_google_favicon=get_google_favicon, user_id=USER_ID)

@app.route('/words')
def words():
    all_words = scoring_words.get_all_user_words()
    return render_template('words.html', words=all_words, user_id=USER_ID)

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

@app.route('/websites')
def websites():
    all_websites = scoring_words.get_all_websites()
    return render_template('websites.html', websites=all_websites, user_id=USER_ID)

@app.route('/websites/add', methods=['POST'])
def add_website():
    url = request.form.get('url')
    refresh_time = int(request.form.get('refresh_time', 60))
    language = request.form.get('language', 'da')
    scoring_words.add_website(url, refresh_time, language)
    return redirect(url_for('websites'))

@app.route('/websites/toggle', methods=['POST'])
def toggle_website():
    url = request.form.get('url')
    active = request.form.get('active') == '1'
    scoring_words.update_website_status(url, active)
    return redirect(url_for('websites'))

@app.route('/websites/delete', methods=['POST'])
def delete_website():
    url = request.form.get('url')
    scoring_words.delete_website(url)
    return redirect(url_for('websites'))

def get_system_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    # Basic article counts
    cursor.execute("SELECT COUNT(*) FROM articles")
    stats['total_articles'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE title IS NULL")
    stats['pending_downloads'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE title IS NOT NULL")
    stats['downloaded_articles'] = cursor.fetchone()[0]
    
    # Processing status
    cursor.execute("SELECT COUNT(*) FROM articles WHERE score = 0")
    stats['unscored_articles'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE rewrite_text IS NULL")
    stats['unrewritten_articles'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE score IS NOT NULL AND rewrite_text IS NOT NULL")
    stats['processed_articles'] = cursor.fetchone()[0]
    
    # Scoring stats
    cursor.execute("SELECT AVG(score) FROM articles WHERE score IS NOT NULL")
    stats['avg_score'] = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE score > 0")
    stats['positive_scores'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE score < 0")
    stats['negative_scores'] = cursor.fetchone()[0]
    
    # Website stats
    cursor.execute("SELECT COUNT(*) FROM websites WHERE active = 1")
    stats['active_websites'] = cursor.fetchone()[0]
    
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM articles WHERE date(publish_date) = ?", (today,))
    stats['articles_today'] = cursor.fetchone()[0]
    
    last_48h = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("SELECT COUNT(*) FROM articles WHERE publish_date > ?", (last_48h,))
    stats['articles_last_24h'] = cursor.fetchone()[0]
    
    # Language distribution
    stats['language_distribution'] = {}
    for lang in ['da', 'en']:
        cursor.execute("""
            SELECT COUNT(a.id) 
            FROM articles a 
            JOIN websites w ON a.base_url LIKE '%' || w.url || '%'
            WHERE w.language = ?
        """, (lang,))
        stats['language_distribution'][lang] = cursor.fetchone()[0]
    
    # System health
    stats['system_healthy'] = (
        stats['pending_downloads'] < stats['total_articles'] * 0.5 and
        stats['unscored_articles'] < stats['total_articles'] * 0.3
    )
    
    # Database size
    stats['db_size'] = f"{os.path.getsize(DB_PATH) / (1024*1024):.2f} MB"
    
    conn.close()
    return stats

@app.route('/status')
def status():
    stats = get_system_stats()
    return render_template('status.html', stats=stats, user_id=USER_ID)

def start_flask():
    """Start the Flask app with environment variables."""
    print(f"Starting Flask app for user {USER_ID} on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=True)

if __name__ == '__main__':
    # get database path from start parameters
    import sys
    if len(sys.argv) < 3:
        print("Usage: python app.py <db_path> <port> <user_id>")
        sys.exit(1)
    HOST = '192.168.86.67'
    DB_PATH = sys.argv[1]
    PORT = sys.argv[2] 
    USER_ID = sys.argv[3] 
    print(f"Starting app with db_path={DB_PATH}, port={PORT}, user_id={USER_ID}")

    scoring_words = ScoringWords(db_path=DB_PATH)

    # Prepare the database
    prepare_db(DB_PATH)

    start_flask()
