import re
import json

# Stopwords list (only common Hindi words, removing duplicates and English homographs like 'the')
STOPWORDS = set([
    'hai', 'ka', 'ke', 'ki', 'ko', 'se', 'mein', 'par', 'aur', 'bhi', 'ye', 'wo', 'jo', 'ki', 'tha', 'thi', 'ne', 'kar', 'kare',
    'karta', 'karti', 'karte', 'karti', 'raha', 'rahi', 'rahe', 'rahi', 'gaya',
    'gayi', 'gaye', 'gayi', 'hota', 'hoti', 'hote', 'hoti', 'hoga', 'hogi',
    'honge', 'hongi', 'ho', 'hoon', 'hain', 'hun', 'thun', 'kya', 'farak'
])

# Common Hindi words in Latin script for detection (only true Hindi words, not English homographs or programming terms)
HINDI_LATIN = set([
    'hai', 'ka', 'ke', 'ki', 'ko', 'se', 'mein', 'par', 'aur', 'bhi', 'ye', 'wo', 'jo', 'ki', 'tha', 'thi', 'ne', 'kar', 'kare',
    'karta', 'karti', 'karte', 'karti', 'raha', 'rahi', 'rahe', 'rahi', 'gaya',
    'gayi', 'gaye', 'gayi', 'hota', 'hoti', 'hote', 'hoti', 'hoga', 'hogi',
    'honge', 'hongi', 'ho', 'hoon', 'hain', 'hun', 'thun', 'kya', 'farak'
])

def detect_language(text):
    # Simple heuristic: count English vs Hindi words from original text
    english_words = 0
    hindi_words = 0
    words = re.findall(r'\b\w+\b', text.lower())  # Split into words, ignoring punctuation
    for word in words:
        if re.match(r'^[a-z]+$', word):  # Only lowercase letters
            if word in HINDI_LATIN:
                hindi_words += 1
            else:
                english_words += 1
        elif re.match(r'^[\u0900-\u097F]+$', word):  # Devanagari script
            hindi_words += 1
    if english_words > 0 and hindi_words > 0:
        return "mixed"
    elif hindi_words > english_words:
        return "hi"
    else:
        return "en"

def is_code_mixed(text):
    lang = detect_language(text)
    return lang == "mixed"

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s\u0900-\u097F]', '', text)  # Keep letters, spaces, and Devanagari
    # Remove stopwords
    words = text.split()
    words = [word for word in words if word not in STOPWORDS]
    # Replace multiple spaces with one
    text = ' '.join(words)
    return text

def preprocess(text):
    original_text = text
    cleaned_text = clean_text(text)
    is_code_mixed_flag = is_code_mixed(text)
    detected_language = detect_language(text)
    return {
        "original_text": original_text,
        "cleaned_text": cleaned_text,
        "is_code_mixed": is_code_mixed_flag,
        "detected_language": detected_language
    }

if __name__ == "__main__":
    # Example usage
    sample_text = input("Enter text to preprocess: ")
    result = preprocess(sample_text)
    print(json.dumps(result, indent=4, ensure_ascii=False))
