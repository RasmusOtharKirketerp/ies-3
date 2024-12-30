from pipeline_helper import fetch_id_and_text_from_articles, fetch_id_and_text_from_articles_with_no_score
from scoring_words import ScoringWords
import sqlite3

import re
from collections import Counter

def score_text(text, scoring_words):
    if not text:
        return -100000
    
    # Normalize the text: convert to lowercase and tokenize
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)  # Extract words as tokens
    token_counts = Counter(tokens)  # Count occurrences of each word

    # Calculate the score
    total_score = 0
    hits = 0
    for word, weight in scoring_words:
        word = word.lower()  # Ensure case-insensitive matching
        if word in token_counts:
            hits += token_counts[word]
            total_score += float(weight) * token_counts[word]
    
    # Normalize score by text length if necessary
    #if len(tokens) > 0:
    #    total_score /= len(tokens)
    return total_score

def get_website_language(url, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM websites WHERE ? LIKE "%" || url || "%"', (url,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'da'  # default to Danish if not found

def score_articles_in_db(db_path):
    sw = ScoringWords(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, text, base_url FROM articles where score IS NULL')
    
    articles = cursor.fetchall()

    for article_id, text, base_url in articles:
        language = get_website_language(base_url, db_path)
        words = sw.get_words_by_language(language)
        score = score_text(text, words)
        if score == 0:
            print('Score is 0 for article with ID:', article_id)
            score = 0.0001
        
        cursor.execute('''
            UPDATE articles SET score=? WHERE id=?
        ''', (score, article_id))
        conn.commit()

    conn.close()

if __name__ == '__main__':
    score_articles_in_db('data/articles.db')
