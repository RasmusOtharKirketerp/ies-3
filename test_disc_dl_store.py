import unittest
from discover_articles import discover_articles
from downloan_articles import download_article
from save_raw_article import store_article
import os
import sqlite3

class TestArticleWorkflow(unittest.TestCase):
    def setUp(self):
        self.base_url = 'https://nyheder.tv2.dk/'
        self.db_path = 'test_articles.db'
        # Remove the test database if it exists
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        # Clean up the test database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_discover_download_store(self):
        # Discover articles
        article_urls = discover_articles(self.base_url)
        self.assertGreater(len(article_urls), 0, "No articles discovered")

        # Download the first article
        article_data = download_article(article_urls[0])
        print(article_data)
        self.assertIn('url', article_data)
        self.assertIn('title', article_data)
        self.assertIn('authors', article_data)
        self.assertIn('publish_date', article_data)
        self.assertIn('text', article_data)
        self.assertIn('top_image', article_data)

        # Store the article
        store_article(article_data, db_path=self.db_path)

        # Verify the article is stored in the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE url=?", (article_data['url'],))
        stored_article = cursor.fetchone()
        print(stored_article)
        conn.close()

        self.assertIsNotNone(stored_article, "Article not stored in the database")
        self.assertEqual(stored_article[1], article_data['url'])
        self.assertEqual(stored_article[2], article_data['title'])

if __name__ == '__main__':
    unittest.main()
