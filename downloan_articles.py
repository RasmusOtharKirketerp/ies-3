from newspaper import Article
from datetime import datetime

def download_article(url):
    article = Article(url)
    article.download()
    article.parse()
    #if no publish date is found, set it to now
    if not article.publish_date:
        article.publish_date = datetime.now()
    return {
        'url': url,
        'title': article.title,
        'authors': article.authors,
        'publish_date': article.publish_date,
        'text': article.text,
        'top_image': article.top_image
    }

if __name__ == '__main__':
    article_data = download_article('https://nyheder.tv2.dk/samfund/2024-12-24-familie-var-centimeter-fra-at-blive-paakoert-det-var-helt-sindssygt')
    print(article_data)
