import datetime
import json
import os
from preprocess import preprocess
from semantic_analysis import analyze_intent
from translation import translate_code_mixed_text

# Path to the JSON file for storing inputs
INPUTS_FILE = 'backend/inputs/inputs.json'

def load_inputs():
    if os.path.exists(INPUTS_FILE):
        with open(INPUTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_inputs(inputs):
    with open(INPUTS_FILE, 'w') as f:
        json.dump(inputs, f, indent=4)

def generate_response(intent_data):
    """
    Generate a templated response based on the intent.
    Returns a JSON object with response_text, intent, and timestamp.
    """
    intent = intent_data['intent']
    if intent == 'concept_explanation':
        response_text = "This looks like a conceptual question. I’ll fetch a clear explanation for you soon."
    elif intent == 'debug_help':
        response_text = "You’re asking for help with an error or bug. Debug assistant coming next."
    elif intent == 'code_output_prediction':
        response_text = "You want to predict the output of some code. Output simulator will handle this soon."
    elif intent == 'general_question':
        response_text = "General question noted. I’ll route this to the learning assistant in the next phase."
    else:
        response_text = "Intent not recognized."
    timestamp = datetime.datetime.now().isoformat()
    return {
        "response_text": response_text,
        "intent": intent,
        "timestamp": timestamp
    }

def main():
    # Delete old inputs file if exists and create a new empty one
    if os.path.exists(INPUTS_FILE):
        os.remove(INPUTS_FILE)
    save_inputs([])  # Create new empty file
    stored_inputs = []
    print("Welcome to CodeBhasha MVP CLI Assistant.")
    print("Enter your queries about code or logic. Type 'exit' to quit.")
    while True:
        user_input = input("Enter your query: ").strip()
        if user_input.lower() == 'exit':
            break
        if user_input:
            timestamp = datetime.datetime.now().isoformat()
            preprocessed = preprocess(user_input)
            # Add translation if code-mixed
            if preprocessed.get('is_code_mixed', False):
                translated_text = translate_code_mixed_text(preprocessed['original_text'])
                preprocessed['translated_text'] = translated_text
            intent_analysis = analyze_intent(preprocessed)
            response = generate_response(intent_analysis)
            stored_inputs.append({
                'input': user_input,
                'timestamp': timestamp,
                'preprocessed': preprocessed,
                'intent': intent_analysis,
                'response': response
            })
            save_inputs(stored_inputs)
            print("Input saved successfully.")
            # Print preprocessed info
            lang_map = {"en": "full english", "hi": "full hindi", "mixed": "hinglish"}
            detected = preprocessed["detected_language"]
            print(f"Detected: {lang_map.get(detected, detected)}")
            # Print response
            print(f"Response: {response['response_text']}")
        # Ignore empty inputs

if __name__ == "__main__":
    main()
