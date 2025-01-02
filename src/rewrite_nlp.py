#fetch all articles from the database
#rewrite the articles with the nlp from newpaper3k
#store the rewritten articles in the database

import db_layer
import utils
from newspaper import Article
import nltk
nltk.download('punkt_tab')

def rewrite_all_nlp():
    articles = db_layer.fetch_all_articles(utils.PATH_TO_SHARE_DB)
    for article in articles:
        id = article[0]
        new_article = utils.convert_article_from_db_to_newspaper_article(article) 
        new_article.nlp()
        print('*'*50)
        print(new_article.title)
        print(new_article.summary)
        db_layer.update_rewrite_text_by_id(id, new_article.summary, utils.PATH_TO_SHARE_DB)
        #print(new_article.keywords)
    
if __name__ == '__main__':
    rewrite_all_nlp()