import tqdm
import sqlite3
from typing import List, Tuple

class ScoringWords:
    def __init__(self, db_path: str = 'articles.db'):
        self.db_path = db_path
        self._create_table()
        self._create_websites_table()  # Add this line

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scoring_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_da TEXT NOT NULL,
                word_en TEXT NOT NULL,
                weight FLOAT NOT NULL,
                category TEXT,
                UNIQUE(word_da, word_en)
            )
        ''')
        conn.commit()
        conn.close()

    def _create_websites_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS websites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE,
                refresh_time INTEGER NOT NULL,
                language TEXT NOT NULL,
                active BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()

    def add_word(self, word_da: str, word_en: str, weight: float, category: str = "user-word") -> bool:
        word_da = self._clean_word(word_da)
        word_en = self._clean_word(word_en)
        try:
            category = category.lower()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scoring_words (word_da, word_en, weight, category)
                VALUES (?, ?, ?, ?)
            ''', (word_da.lower(), word_en.lower(), weight, category))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def get_all_user_words(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT word_da, word_en, weight, category FROM scoring_words WHERE category="user-word"')
        words = cursor.fetchall()
        conn.close()
        return words

    def get_all_words(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT word_da, word_en, weight, category FROM scoring_words')
        words = cursor.fetchall()
        conn.close()
        return words

    def get_words_by_language(self, language: str = 'da') -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        column = 'word_da' if language.lower() == 'da' else 'word_en'
        cursor.execute(f'SELECT {column}, weight FROM scoring_words')
        words = cursor.fetchall()
        conn.close()
        return words

    def update_word(self, word_da: str, word_en: str, new_word_da: str, new_word_en: str) -> bool:
        new_word_da = self._clean_word(new_word_da)
        new_word_en = self._clean_word(new_word_en)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE scoring_words 
            SET word_da = ?, word_en = ? 
            WHERE word_da = ? AND word_en = ?
        ''', (new_word_da.lower(), new_word_en.lower(), word_da.lower(), word_en.lower()))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def update_weight(self, word_da: str, word_en: str, new_weight: float) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE scoring_words 
            SET weight = ? 
            WHERE word_da = ? AND word_en = ?
        ''', (new_weight, word_da.lower(), word_en.lower()))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def delete_word(self, word_da: str, word_en: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM scoring_words 
            WHERE word_da = ? AND word_en = ?
        ''', (word_da.lower(), word_en.lower()))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def populate_sample_words(self):
        sample_words = [
            ("krig", "war", -0.8, "user-word"),
            ("fred", "peace", 0.6, "user-word"),
            ("død", "death", -0.7, "user-word"),
            ("kærlighed", "love", 0.8, "user-word"),
            ("had", "hate", -0.6, "user-word"),
            ("glæde", "joy", 0.7, "user-word")
        ]
        for word in sample_words:
            self.add_word(word[0], word[1], word[2], word[3])

    def import_from_translation_cache(self, cache_file_path: str = 'translation_cache1000.json') -> int:
            """
            Import words from translation cache JSON file.
            Returns number of words imported successfully.
            """
            try:
                import json
                with open(cache_file_path, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    
                count = 0
                if 'da-en' in cache:
                    for word_da, word_en in tqdm.tqdm(cache['da-en'].items(), desc="Importing words"):
                        #print(f"Adding {word_da} - {word_en}")
                        # Set neutral weight initially (can be updated later)
                        weight = -99999
                        
                        # Try to add the word pair
                        if self.add_word(word_da, word_en, weight, 'translation-cache'):
                            count += 1
                            
                return count
                
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"Error importing from translation cache: {e}")
                return 0
    
    def _clean_word(self, word: str) -> str:
        """Remove common punctuation marks from words."""
        return word.strip(',.!?:;\"\'')

    def add_website(self, url: str, refresh_time: int, language: str = 'da') -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO websites (url, refresh_time, language)
                VALUES (?, ?, ?)
            ''', (url, refresh_time, language))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def get_all_websites(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT url, refresh_time, language, active FROM websites')
        websites = cursor.fetchall()
        conn.close()
        return websites

    def update_website_status(self, url: str, active: bool) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE websites 
            SET active = ? 
            WHERE url = ?
        ''', (active, url))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def delete_website(self, url: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM websites WHERE url = ?', (url,))
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
        except sqlite3.Error:
            return False

    def populate_sample_websites(self):
        websites = {
            'https://nyheder.tv2.dk/': ('da', 60),
            'https://www.dr.dk/nyheder/': ('da', 60),
            'https://cnn.com/': ('en', 60),
            'https://www.bt.dk/': ('da', 60),
            'https://ekstrabladet.dk/': ('da', 60),
            'https://www.berlingske.dk/': ('da', 60),
            'https://www.version2.dk/': ('da', 60),
            'https://www.computerworld.dk/': ('da', 60),
        }
        for url, (lang, refresh) in websites.items():
            self.add_website(url, refresh, lang)

if __name__ == '__main__':
    scoring_words = ScoringWords()
    scoring_words.populate_sample_words()
    words = scoring_words.get_all_words()
    print(words)
    words_da = scoring_words.get_words_by_language('da')
    print(words_da)
    words_en = scoring_words.get_words_by_language('en')
    print(words_en)
    scoring_words.update_weight('krig', 'war', -0.9)
    words = scoring_words.get_all_words()
    print(words)
    scoring_words.delete_word('krig', 'war')
    words = scoring_words.get_all_words()
    print(words)
    #add all words from translation_cache1000.json with wiehgts of 0.5
    scoring_words.import_from_translation_cache()
    scoring_words.populate_sample_websites()
    websites = scoring_words.get_all_websites()
    print(websites)


