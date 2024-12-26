from pipeline_helper import fetch_id_and_text_from_articles, fecth_article_txt_by_id
import sqlite3

def score_text(text, pos_words, neg_words):
    #lowercase the text
    text = text.lower()

    score = 0
    for word in pos_words:
        #if the word is a positive word, or part of a positive word add 1 to the score
        if word in text:
            score += 1
            print(f"Positive word found: {word}")
    
    for word in neg_words:
        if word in text:
            score -= 10000
            print(f"Negative word found: {word}")

    return score

def score_articles_in_db(db_path='articles.db'):
    positive_words = [
        "usa", "trump", "skizotypi", "quetiapin", "mette", "løb", "brætspil", "musik", "udvikling",
        "programmering", "neuralnetværk", "computerspil", "kaffe", "carnivore", "sundhed","elon","musk"
        "mentalitet", "videnskab", "historie", "læring", "humor", "filmredigering", "forskning",
        "søvn", "træning", "kreativitet", "teknologi", "frihed", "matematik", "garmin", "podcast", "ukraine",
        "klima", "politik", "filosofi", "kunstigintelligens", "kommunikation", "kultur", "bøger", "natur",
        "fysik", "kemi", "biologi", "psykologi", "sociologi", "økonomi", "filosofi", "religion", "etik",
        "moral", "retfærdighed", "køn", "racisme", "feminisme",  
    ]
    
    negative_words = ["lgbtq", "feminisme", "fifa"]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    articles = fetch_id_and_text_from_articles(db_path)
    for article_id, text in articles:
        score = score_text(text, positive_words, negative_words)
        cursor.execute('''
            UPDATE articles SET score=? WHERE id=?
        ''', (score, article_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    score_articles_in_db()
