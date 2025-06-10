#useing ollama to read all articles in the db and rewrite them
import db_layer
from ollama_interface import query_ollama

def count_words(text):
    return len(text.split())

a = db_layer.TEST_get_10_articles_with_text(db_path='share_articles.db')

sytemPrompt = 'You are an articles rewriter. Please write a short resume on max 50 words. Answer ONLY text.'
#sytemPrompt = 'Du er Dansk journalistisk omskriver. Skriv et meget kort resume. Ikke mere end 50 ord:'
print('Rewriting articles')
for article in a:
    t = article[5]
    print('*'*150)
    t_words = count_words(t)
    print('Original article :')
    print(t[:70])
    prefix_prompt = 'Here is the article you need to rewrite'
    response = query_ollama(system_prompt = sytemPrompt, prompt = prefix_prompt+t)
    print('Rewritten article:')
    print('-'*150)
    responce_words = count_words(response)
    print(response)
    print('-'*150)
    print(f'Original article has {t_words} words and rewritten article has {responce_words} words, that a procentage of {responce_words/t_words*100:.2f}%')
