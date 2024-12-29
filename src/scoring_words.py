import tqdm
import sqlite3
from typing import List, Tuple

class ScoringWords:
    def __init__(self, db_path: str = 'articles.db'):
        self.db_path = db_path
        self._create_table()

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

    def add_word(self, word_da: str, word_en: str, weight: float, category: str = None) -> bool:
        word_da = self._clean_word(word_da)
        word_en = self._clean_word(word_en)
        try:
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
            ("krig", "war", -0.8, "conflict"),
            ("fred", "peace", 0.6, "harmony"),
            ("død", "death", -0.7, "negative"),
            ("kærlighed", "love", 0.8, "positive"),
            ("had", "hate", -0.6, "negative"),
            ("glæde", "joy", 0.7, "positive")
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
                        if self.add_word(word_da, word_en, weight):
                            count += 1
                            
                return count
                
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"Error importing from translation cache: {e}")
                return 0
    
    def _clean_word(self, word: str) -> str:
        """Remove common punctuation marks from words."""
        return word.strip(',.!?:;\"\'')

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


