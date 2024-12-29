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


def score_articles_in_db(db_path='articles.db', rescoring=False):
    sw = ScoringWords()
    words = sw.get_words_by_language('da')  # Get Danish words with their weights

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    articles = []
    if rescoring:
        articles = fetch_id_and_text_from_articles()
    else:
        articles = fetch_id_and_text_from_articles_with_no_score(db_path)

    for article_id, text in articles:
        score = score_text(text, words)
        cursor.execute('''
            UPDATE articles SET score=? WHERE id=?
        ''', (score, article_id))
        conn.commit()

    conn.close()

if __name__ == '__main__':
    score_articles_in_db(rescoring=True)
