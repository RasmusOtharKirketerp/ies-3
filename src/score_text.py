from scoring_words import ScoringWords
import re
from collections import Counter
import db_layer

def score_text(text, scoring_words, debug=False):
    if not text:
        return -100000
    
    # Normalize the text: convert to lowercase and tokenize
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)  # Extract words as tokens
    if debug:
        print(tokens)
    token_counts = Counter(tokens)  # Count occurrences of each word
    if debug:
        print(token_counts)

    # Calculate the score
    total_score = 0
    hits = 0
    for word, weight in scoring_words:
        word = word.lower().strip()  # Ensure case-insensitive matching and remove whitespace
        # Match partial words
        matching_tokens = [token for token in tokens if word in token]
        for token in matching_tokens:
            count = token_counts[token]
            if debug:
                print(f"Word '{word}' matched in token '{token}' with weight {weight} and count {count}")
            hits += count
            total_score += float(weight) * count
    
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
