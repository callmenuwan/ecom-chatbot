# chatbot/nlp/intent_engine.py

import spacy
import json
import os
from deep_translator import GoogleTranslator
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load model and preprocessors
model = load_model("nlp/training/intent_model.h5")
with open("nlp/training/tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

with open("nlp/training/label_encoder.pickle", "rb") as enc:
    lbl_encoder = pickle.load(enc)

# Parameters (same used in training)
max_len = 20

# Load intents for response lookup (optional)
with open("nlp/training/intents.json") as file:
    intents_data = json.load(file)

def predict_intent(user_input):
    seq = tokenizer.texts_to_sequences([user_input])
    padded = pad_sequences(seq, truncating='post', maxlen=max_len)
    predictions = model.predict(padded, verbose=0)
    intent_index = np.argmax(predictions)
    intent_tag = lbl_encoder.inverse_transform([intent_index])[0]
    confidence = float(np.max(predictions))

    # Get response from intents.json
    response = "I'm not sure how to respond."
    for intent in intents_data['intents']:
        if intent['tag'] == intent_tag:
            response = np.random.choice(intent['responses'])
            break
        
    return intent_tag, confidence, response




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
