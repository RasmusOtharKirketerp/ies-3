#utils.py
from newspaper import Article
import db_layer

#CONSTANTS
PATH_TO_SHARE_DB = 'share_articles.db'
PATH_TO_RASMUS_DB = 'rasmus_articles.db'
PATH_TO_METTE_DB = 'mette_articles.db'

#These URL contains a list of latest news and should be excluded, because they changes all the time
EXCLUDE_URLS = ["https://www.dr.dk/nyheder/seneste", "https://nyheder.tv2.dk/seneste"]

def convert_article_from_db_to_newspaper_article(articleDB):
    new_article = Article(articleDB[1])
    new_article.title = articleDB[2]
    new_article.authors = articleDB[3]
    new_article.publish_date = articleDB[4]
    new_article.text = articleDB[5]
    new_article.top_image = articleDB[6]
    new_article.download_state = 2  # ArticleDownloadState.SUCCESS
    new_article.is_parsed = True
    return new_article

if __name__ == '__main__':
    a10 = db_layer.TEST_get_10_articles_with_text(PATH_TO_SHARE_DB)
    for a in a10:
        b = convert_article_from_db_to_newspaper_article(a)
        print("Title", b.title)
        print("Text", b.text)