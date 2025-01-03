#this test is to test the article score function
import db_layer
import utils

from score_text import score_text
from scoring_words import ScoringWords
test_articles = db_layer.TEST_get_1_fecth_all_id_and_text_and_base_url_from_url('https://nyheder.tv2.dk/udland/2024-12-29-ny-leder-vil-afholde-valg-inden-for-de-naeste-fire-aar-i-syrien',utils.PATH_TO_SHARE_DB)

sw = ScoringWords(utils.PATH_TO_RASMUS_DB)

for id, text, base_url in test_articles:
    print(id)
    print(text)
    print('*'*50)
    print()
    language = db_layer.get_website_language(base_url, utils.PATH_TO_SHARE_DB)
    words = sw.get_words_by_language(language)
    score = score_text(text, words, debug=True)
    print("Rasmus words : ", words)
    print(score)