import requests
import json
import time

class TranslationHelper:
    def __init__(self):
        self.base_url = "https://translate.googleapis.com/translate_a/single"
        self.cache_file = "translation_cache1000.json"
        self.load_cache()

    def load_cache(self):
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.cache = {"da-en": {}}

    def save_cache(self):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def translate(self, text, src='da', dest='en'):
        cache_key = f"{src}-{dest}"
        if text in self.cache.get(cache_key, {}):
            return self.cache[cache_key][text]

        params = {
            'client': 'gtx',
            'sl': src,
            'tl': dest,
            'dt': 't',
            'q': text
        }

        try:
            response = requests.get(self.base_url, params=params)
            result = response.json()[0][0][0]
            
            if cache_key not in self.cache:
                self.cache[cache_key] = {}
            self.cache[cache_key][text] = result
            self.save_cache()
            
            time.sleep(0.5)  # Be nice to the API
            return result
        except Exception as e:
            print(f"Translation error: {e}")
            return text
