from newspaper import build

def discover_articles(base_url):
    # Build the newspaper source
    paper = build(base_url, memoize_articles=False)
    
    # Filter articles to include only those starting with base_url
    article_urls = [article.url for article in paper.articles if article.url.startswith(base_url)]
    
    return article_urls

if __name__ == '__main__':
    base_url = 'https://nyheder.tv2.dk/'
    urls = discover_articles(base_url)

    print(urls)
