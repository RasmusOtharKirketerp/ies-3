from newspaper import build

def discover_articles(base_url):
    paper = build(base_url, memoize_articles=False)
    article_urls = [article.url for article in paper.articles]
    return article_urls

if __name__ == '__main__':
    base_url = 'https://nyheder.tv2.dk/'
    urls = discover_articles(base_url)

    print(urls)