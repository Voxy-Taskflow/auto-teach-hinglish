import json
import os
from transformers import pipeline

# Use Helsinki-NLP model for Hindi to English translation
TRANSLATION_PIPELINE = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")

# Cache file path
CACHE_FILE = 'backend/cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4, ensure_ascii=False)

def translate_code_mixed_text(text):
    """
    Translate code-mixed text (Romanized Hindi) to English using Helsinki-NLP model.
    Uses caching to avoid re-translation.
    """
    cache = load_cache()
    if text in cache:
        return cache[text]

    # Translate directly (model handles Romanized Hindi)
    result = TRANSLATION_PIPELINE(text)
    translated_text = result[0]['translation_text']

    # Cache the result
    cache[text] = translated_text
    save_cache(cache)

    return translated_text
