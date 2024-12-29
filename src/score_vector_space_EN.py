import nltk
from gensim.models import KeyedVectors
import gensim.downloader as api
from numpy import dot
from numpy.linalg import norm
from googletrans import Translator
from collections import Counter
import json
import os
import numpy as np
from collections import defaultdict
from translation_helper import TranslationHelper

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
cache_file = 'translation_cache1000.json'

def load_translation_cache():
    """Load the translation cache from file"""
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_translation_cache(cache):
    """Save the translation cache to file"""
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save translation cache: {e}")

translator = TranslationHelper()

def translate_text(text, source_lang='da', target_lang='en'):
    """Translate text word by word using cache"""
    words = text.split()
    translated_words = translate_words(words, source_lang, target_lang)
    return ' '.join(translated_words)

def translate_words(words, source_lang='da', target_lang='en'):
    """Translate a list of words to target language using cache"""
    # Load cache
    cache = load_translation_cache()
    cache_key = f"{source_lang}-{target_lang}"
    if cache_key not in cache:
        cache[cache_key] = {}
    
    translated = []
    cache_modified = False
    cache_hits = 0
    cache_misses = 0

    for word in words:
        word_lower = word.lower()
        # Check if word is in cache
        if word_lower in cache[cache_key]:
            translated.append(cache[cache_key][word_lower])
            cache_hits += 1
            print(f"Cache hit for word '{word}'")
        else:
            try:
                trans = translator.translate(word, src=source_lang, dest=target_lang)
                translated_word = trans.text.lower()
                # Add to cache
                print(f"Added to cache word '{word}', translated to '{translated_word}'")
                cache[cache_key][word_lower] = translated_word
                translated.append(translated_word)
                cache_modified = True
                cache_misses += 1
            except Exception as e:
                print(f"Warning: Translation failed for word '{word}': {e}")
                translated.append(word_lower)

    # Save cache if modified
    if cache_modified:
        save_translation_cache(cache)
        print(f"Translation cache stats - Hits: {cache_hits}, Misses: {cache_misses}")

    return translated

def score_text_using_vector(text, word_list, weights, lang):
    """
    Score text based on semantic similarity to weighted word list.
    """

    # validate if length of word_list and weights are the same
    if len(word_list) != len(weights):
        print("Error: Length of word_list and weights must be the same")
        return 0
    if lang == 'da':
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('danish'))
        # Translate Danish words to English for better model coverage
        word_list = translate_words(word_list, 'da', 'en')
        text = translate_text(text, 'da', 'en')
    else:
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))

    lemmatizer = nltk.WordNetLemmatizer()
    
    # Use word2vec model for better word coverage
    model = api.load('word2vec-google-news-300')

    # Process text
    text_words = [lemmatizer.lemmatize(word) for word in text.lower().split() if word not in stop_words]
    # Count word frequencies
    word_freq = Counter(text_words)
    
    # Get vectors for words that exist in model
    text_vectors = [(model[word], word_freq[word]) 
                   for word in text_words 
                   if word in model]
    
    if not text_vectors:
        print(f"Warning: No words from the text were found in the model's vocabulary")
        return 0

    def cosine_similarity(vec1, vec2):
        return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

    score = 0
    comparison_count = 0
    similarity_threshold = 0.5  # Increased from 0.3 to 0.5 for stricter matching
    max_words_to_consider = 20  # Limit words to prevent length bias
    
    for i, target_word in enumerate(word_list):
        target_word = lemmatizer.lemmatize(target_word.lower())
        if target_word in model:
            word_vector = model[target_word]
            word_scores = []
            
            # Get top N most relevant words from text
            word_similarities = []
            for text_vector, freq in text_vectors:
                similarity = cosine_similarity(word_vector, text_vector)
                if similarity > similarity_threshold:
                    word_similarities.append((similarity, freq))
            
            # Sort by similarity and take top words
            word_similarities.sort(reverse=True)
            top_similarities = word_similarities[:max_words_to_consider]
            
            if top_similarities:
                # Calculate weighted average of similarities
                total_sim = 0
                total_weight = 0
                for sim, freq in top_similarities:
                    # Apply exponential weighting to favor higher similarities
                    weight = freq * (sim ** 2)  # Square similarity for more emphasis on close matches
                    total_sim += sim * weight
                    total_weight += weight
                    comparison_count += 1
                
                if total_weight > 0:
                    avg_similarity = total_sim / total_weight
                    score += weights[i] * avg_similarity

        else:
            print(f"Warning: Word '{target_word}' not found in model vocabulary")

    # Normalize score
    if comparison_count > 0:
        score = score / (len(word_list) * max(1, len(text_words) / 100))  # Normalize by text length

    print(f"Language: {lang}")
    print(f"Text: {text[:200]}...")
    print(f"Words found in model: {len(text_vectors)}/{len(text_words)}")
    print(f"Word list: {word_list}", f"Weights: {weights}")
    print(f"Score: {score:.4f}")
    return score

def fetch_id_and_text_from_articles(db_path, limit=10):
    """Fetch article IDs and texts from the database"""
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM articles LIMIT ?", (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

if __name__ == '__main__':
  # Example usage remains the same
  #text_in_EN = "This is an example text about machine learning."
  #text_in_EN = "Once upon a time, there was a lady in the forest. The lady was very beautiful and she was very kind. She was always helping the animals in the forest. The animals loved her very much. One day, the lady found a little bird with a broken wing. She took the bird home and took care of it. The bird was very happy and it sang beautiful songs for the lady. The lady was very happy too. She loved the bird very much. The bird stayed with the lady and they became best friends. The lady and the bird lived happily ever after."
  #word_list_EN = ["machine", "learning", "artificial", "intelligence"]
  #word_list_EN2 = ["cheese", "food", "pizza", "dough"]
  #word_list_EN3 = ["lady", "bird", "forest", "beautiful"]

  #text_in_DA = "Dette er en eksempeltekst om kunstig maskinlæring. Maskinlæring er en gren af kunstig intelligens, der fokuserer på at udvikle algoritmer og teknikker, der giver computere mulighed for at lære."
  #word_list_DA = ["maskine", "læring", "kunstig", "intelligens"]

  #weights = [1, 1, 0.5, 0.5]

  #score = score_text_using_vector(text_in_DA, word_list_DA, weights, 'da')
  #score = score_text_using_vector(text_in_EN, word_list_EN, weights, 'en')
  #score = score_text_using_vector(text_in_EN, word_list_EN2, weights, 'en')
  #score = score_text_using_vector(text_in_EN, word_list_EN3, weights, 'en')


#fetch 10 articles from the database and score them

  weights = [
      0.7, 0.6, 0.9, 0.8, 0.9, 0.7, 0.8, 0.9, 0.8, 0.9, 0.9, 0.8, 0.7, 0.8, 0.9, 1.0, 1.0, 
      0.8, 0.9, 0.8, 0.8, 0.9, 0.8, 0.7, 0.8, 0.9, 1.0, 0.9, 0.9, 0.8, 0.7, 0.7, 0.8, 0.6, 
      0.9, 1.0, 0.8, 0.8, 0.7, 0.8, 0.9, 0.8, 0.8, 0.8, 0.9, 0.8, 0.7, 0.6, 0.8, 0.8, 0.9, 
      0.7, 0.7, 0.7
  ]

  words = [
          "usa", "trump", "skizotypi", "quetiapin", "mette", "løb", "brætspil", "musik", "udvikling",
          "programmering", "neuralnetværk", "computerspil", "kaffe", "carnivore", "sundhed","elon","musk"
          "mentalitet", "videnskab", "historie", "læring", "humor", "filmredigering", "forskning",
          "søvn", "træning", "kreativitet", "teknologi", "frihed", "matematik", "garmin", "podcast", "ukraine",
          "klima", "politik", "filosofi", "kunstigintelligens", "kommunikation", "kultur", "bøger", "natur",
          "fysik", "kemi", "biologi", "psykologi", "sociologi", "økonomi", "filosofi", "religion", "etik",
          "moral", "retfærdighed", "køn", "racisme", "feminisme",  
          ]


  articles10 = fetch_id_and_text_from_articles(db_path='articles.db', limit=10)
  for article in articles10:
      article_id, text = article
      score = score_text_using_vector(text, words, weights, 'da')
      print(f"Article ID: {article_id}, Score: {score:.4f}")
