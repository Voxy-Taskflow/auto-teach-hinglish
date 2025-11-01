import json
import os
from translation import translate_code_mixed_text

# Path to inputs file
INPUTS_FILE = 'backend/inputs/inputs.json'

def load_inputs():
    if os.path.exists(INPUTS_FILE):
        with open(INPUTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_inputs(inputs):
    with open(INPUTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(inputs, f, indent=4, ensure_ascii=False)

def main():
    inputs = load_inputs()
    updated = False
    for entry in inputs:
        preprocessed = entry.get('preprocessed', {})
        if preprocessed.get('is_code_mixed', False):
            original_text = preprocessed.get('original_text', '')
            if 'translated_text' not in preprocessed and original_text:
                print(f"Translating: {original_text}")
                translated_text = translate_code_mixed_text(original_text)
                preprocessed['translated_text'] = translated_text
                updated = True
                print(f"Translated to: {translated_text}")
    if updated:
        save_inputs(inputs)
        print("Updated inputs.json with translations.")
    else:
        print("No new translations needed.")

if __name__ == "__main__":
    main()
