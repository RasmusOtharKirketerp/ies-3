from newspaper import Article
from datetime import datetime
from urllib.parse import urlparse
import re

def extract_words_from_url(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Get the path component
    path = parsed_url.path
    
    # Split the path into parts and extract words
    path_parts = path.strip('/').split('/')
    words = []
    for part in path_parts:
        # Extract alphanumeric words
        words.extend(re.findall(r'\b\w+\b', part))
    
    # Filter out non-meaningful parts (optional, remove GUIDs or IDs)
    words = [word for word in words if not re.match(r'^[0-9a-f-]+$', word)]
    
    # Join the words into a single string
    return ' '.join(words)

def download_article(url):
    article = Article(url)
    article.download()
    article.parse()
    #if no publish date is found, set it to now
    if not article.publish_date:
        article.publish_date = datetime.now()

    if article.title == '':
        if article.text == '':
            sub = extract_words_from_url(url)
            article.title = "Ingen data fundet. URL data bruges til scoring: " + sub
            article.text = "Brug linket til at finde artiklen. URL bliver brugt til at score med :" + sub

    #if no text is found, set it to the title
    if article.text == '':
        if article.title > '':
            article.text = article.title
    return {
        'url': url,
        'title': article.title,
        'authors': article.authors,
        'publish_date': article.publish_date,
        'text': article.text,
        'top_image': article.top_image
    }

if __name__ == '__main__':
    #article_data = download_article('https://nyheder.tv2.dk/samfund/2024-12-24-familie-var-centimeter-fra-at-blive-paakoert-det-var-helt-sindssygt')
    article_data = download_article('https://play.tv2.dk/event/serie-a-juventus-fiorentina-381eeb9d-f515-4552-aaa8-495ba39ac919')
    print(article_data)
