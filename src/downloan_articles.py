from newspaper import Article
from datetime import datetime
from urllib.parse import urlparse
import re
import time

from save_raw_article import get_cached_articles, chech_if_url_need_download

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

def download_article(url, retries=3, delay=5, db_path='error.db'):
    #chech if the url is already in the database
    if chech_if_url_need_download(url, db_path):
        print(f"URL {url} already in database {db_path}, loading from db")
        article = get_cached_articles(url, db_path)
        return article
    
    for attempt in range(retries):
        try:
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
        except Exception as e:
            print(f"Error downloading article from {url}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to download article from {url} after {retries} attempts.")
                return {
                    'url': url,
                    'title': "Download failed",
                    'authors': [],
                    'publish_date': None,
                    'text': "Failed to download article content.",
                    'top_image': None
                }

if __name__ == '__main__':
    #article_data = download_article('https://nyheder.tv2.dk/samfund/2024-12-24-familie-var-centimeter-fra-at-blive-paakoert-det-var-helt-sindssygt')
    article_data = download_article('https://play.tv2.dk/event/serie-a-juventus-fiorentina-381eeb9d-f515-4552-aaa8-495ba39ac919')
    print(article_data)
