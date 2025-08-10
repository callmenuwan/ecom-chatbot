# train_intent_model.py

import json
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Step 1: Load training data
with open("intents.json") as file:
    data = json.load(file)

training_sentences = []
training_labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        training_sentences.append(pattern)
        training_labels.append(intent["tag"])

# Step 2: Encode labels'
lbl_encoder = LabelEncoder()
training_labels_encoded = lbl_encoder.fit_transform(training_labels)

# Step 3: Tokenize and pad sequences
vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

# Step 4: Build model
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(len(lbl_encoder.classes_), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Step 5: Train
model.fit(padded_sequences, np.array(training_labels_encoded), epochs=200)

# Step 6: Save model and preprocessors
model.save("intent_model.h5")

with open("tokenizer.pickle", "wb") as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open("label_encoder.pickle", "wb") as ecn_file:
    pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

print("✅ Training complete. Model saved as 'intent_model.h5'")