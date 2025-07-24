# chatbot/nlp/intent_engine.py

import spacy
import json
import os

class IntentEngine:
    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm") # Loads spaCy's English model (for tokenization, lemmatization, etc.)

        pattern_path = os.path.join(os.path.dirname(__file__), "patterns.json") # Path to the JSON file containing intent patterns
        with open(pattern_path, "r") as file:
            self.patterns = json.load(file)

    def detect_intent(self, text):
        doc = self.nlp(text.lower()) # Process the input text with spaCy
        
        for intent, keywords in self.patterns.items(): # Iterate through each intent and its associated keywords
            for keyword in keywords: # Check if any keyword is present in the processed text
                if keyword in doc.text: # If keyword is found in the text
                    return intent
        return "unknown"
