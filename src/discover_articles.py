from newspaper import build
from utils import EXCLUDE_URLS

def discover_articles(base_url):
    # Build the newspaper source
    paper = build(base_url, memoize_articles=False)

    DEBUG = False  # Set to True to enable debug output
    # Debug: print articles that do not start with base_url
    if DEBUG:
        for article in paper.articles:
            if not article.url.startswith(base_url):
                print(f"DEBUG: Skipping article with wrong base_url: {article.url}")
            print(f"DEBUG: Found article URL: {article.url}")

    # Filter articles to include only those starting with base_url
    article_urls = [article.url for article in paper.articles if article.url.startswith(base_url)]


    # Exclude URLs from the EXCLUDE_URLS list
    article_urls = [
        url for url in article_urls if not any(excluded in url for excluded in EXCLUDE_URLS)
    ]

    
    return article_urls

if __name__ == '__main__':
    #base_url = 'https://www.dr.dk/nyheder'
    #base_url = 'https://egedalkommune.dk/nyheder'
    base_url = 'https://x.com/KyivPost/status/1934644778446074311'
    urls = discover_articles(base_url)

    print(urls)
