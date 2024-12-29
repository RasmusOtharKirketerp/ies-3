import nltk
from danlp.datasets import cached_path
from danlp.models import load_wv_with_gensim

nltk.download('wordnet')
nltk.download('omw-1.4')

# Hent stien til den cachelagrede model
model_path = cached_path('wikipedia.da')

def score_text(text, word_list, weights):
  """
  Scorer tekst baseret på en liste af ord og deres vægt.

  Args:
    text: Teksten, der skal scores.
    word_list: En liste af ord.
    weights: En liste af vægte, der svarer til ordene i word_list.

  Returns:
    Den samlede score for teksten.
  """
  lemmatizer = nltk.WordNetLemmatizer()
  
  # Indlæs modellen fra den cachelagrede sti
  model = load_wv_with_gensim(model_path) 

  text_words = [lemmatizer.lemmatize(word) for word in text.lower().split()]
  text_vectors = [model.wv[word] for word in text_words if word in model.wv]

  score = 0
  for i, word in enumerate(word_list):
    word = lemmatizer.lemmatize(word)
    if word in model.wv:
      word_vector = model.wv[word]
      for text_vector in text_vectors:
        score += weights[i] * model.wv.similarity(word, text_vector)

  return score

# Eksempel på brug
text = "Dette er en eksempeltekst om maskinlæring."
word_list = ["maskine", "læring", "kunstig", "intelligens"]
weights = [1, 1, 0.5, 0.5]

score = score_text(text, word_list, weights)
print(f"Score: {score}")