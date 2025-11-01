import json

def analyze_intent(preprocessed_data):
    """
    Analyze the preprocessed text to determine the student's intent.
    Returns a JSON object with intent, confidence, and reason.
    """
    cleaned_text = preprocessed_data.get("cleaned_text", "").lower()
    original_text = preprocessed_data.get("original_text", "").lower()

    # Keywords for concept_explanation
    concept_keywords = ["what", "define", "explain", "meaning", "why", "difference", "farq", "kya"]
    # Keywords for debug_help
    debug_keywords = ["error", "fix", "not working", "problem", "bug", "issue"]
    # Keywords for code_output_prediction
    output_keywords = ["output", "result", "print", "display", "show"]

    # Check for concept_explanation
    if any(keyword in cleaned_text or keyword in original_text for keyword in concept_keywords):
        intent = "concept_explanation"
        confidence = 0.9
        reason = f"Detected keyword(s) like '{[k for k in concept_keywords if k in cleaned_text or k in original_text][0]}' indicating conceptual query."
    # Check for debug_help
    elif any(keyword in cleaned_text or keyword in original_text for keyword in debug_keywords):
        intent = "debug_help"
        confidence = 0.85
        reason = f"Detected keyword(s) like '{[k for k in debug_keywords if k in cleaned_text or k in original_text][0]}' indicating debugging assistance."
    # Check for code_output_prediction
    elif any(keyword in cleaned_text or keyword in original_text for keyword in output_keywords):
        intent = "code_output_prediction"
        confidence = 0.8
        reason = f"Detected keyword(s) like '{[k for k in output_keywords if k in cleaned_text or k in original_text][0]}' indicating output prediction."
    # Default to general_question
    else:
        intent = "general_question"
        confidence = 0.6
        reason = "No specific keywords detected, classifying as general question."

    return {
        "intent": intent,
        "confidence": confidence,
        "reason": reason
    }

if __name__ == "__main__":
    # Example usage
    sample_input = json.loads(input("Enter preprocessed JSON: "))
    result = analyze_intent(sample_input)
    print(json.dumps(result, indent=4))
