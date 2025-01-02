from scoring_words import ScoringWords
import sqlite3
import re
from collections import Counter
import db_layer

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



def score_articles_in_db(db_path):
    sw = ScoringWords(db_path)
        
    articles = db_layer.fecth_all_id_and_text_and_base_url(db_path=db_path)

    for id, text, base_url in articles:
        language = db_layer.get_website_language(base_url, db_path)
        words = sw.get_words_by_language(language)
        score = score_text(text, words)
        if score == 0:
            score = 0.0001
        
        db_layer.update_score_by_id(id, score, db_path)


if __name__ == '__main__':
    score_articles_in_db('data/articles.db')
