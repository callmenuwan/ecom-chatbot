# chatbot/nlp/intent_engine.py

import spacy
import json
import os
from deep_translator import GoogleTranslator

class IntentEngine:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        # Load intent keyword patterns
        pattern_path = os.path.join(os.path.dirname(__file__), "patterns.json")
        with open(pattern_path, "r") as file:
            self.patterns = json.load(file)

    def translate_to_english(self, text):
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text)
            return translated
        except Exception as e:
            print("Translation error:", e)
            return text  # fallback to original

    def lemmatize_text(self, text):
        doc = self.nlp(text.lower())
        lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return lemmatized_tokens

    def detect_intent(self, text):
        # Step 1: Translate if needed
        translated_text = self.translate_to_english(text)

        # Step 2: Lemmatize user input
        input_lemmas = self.lemmatize_text(translated_text)

        # Step 3: Compare against lemmatized keywords
        for intent, keywords in self.patterns.items():
            for keyword in keywords:
                keyword_doc = self.nlp(keyword.lower())
                keyword_lemmas = [token.lemma_ for token in keyword_doc if not token.is_stop and not token.is_punct]

                # Check if all keyword lemmas exist in user input lemmas
                if any(k in input_lemmas for k in keyword_lemmas):
                    return intent
        return "unknown"
