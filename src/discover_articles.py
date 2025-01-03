from newspaper import build
from utils import EXCLUDE_URLS

def discover_articles(base_url):
    # Build the newspaper source
    paper = build(base_url, memoize_articles=False)
    
    # Filter articles to include only those starting with base_url
    article_urls = [article.url for article in paper.articles if article.url.startswith(base_url)]

    #exclude this URL from article_urls "https://www.dr.dk/nyheder/seneste" and "https://nyheder.tv2.dk/seneste"
    # Exclude URLs from the EXCLUDE_URLS list
    article_urls = [
        url for url in article_urls if not any(excluded in url for excluded in EXCLUDE_URLS)
    ]

    
    return article_urls

if __name__ == '__main__':
    base_url = 'https://www.dr.dk/nyheder'
    urls = discover_articles(base_url)

    print(urls)
