"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_001.txt
Run      : 2
"""

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import json
import pickle
import numpy as np
from tensorflow.keras.optimizers import SGD
import random
import tkinter as tk
from tkinter import scrolledtext

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents and responses from JSON file
with open('intents.json') as json_data:
    intents = json.load(json_data)

# Load model and data from pickle file
with open('data.pkl', 'rb') as f:
    words, labels, training, output = pickle.load(f)

# Create model
model = Sequential()
model.add(Dense(64, input_shape=(len(training[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(output[0]), activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True), metrics=['accuracy'])

# Train model
model.fit(np.array(training), np.array(output), epochs=200, batch_size=5, verbose=0)

# Function to clean and process user input
def clean_input(user_input):
    user_input = user_input.lower()
    user_input = word_tokenize(user_input)
    user_input = [lemmatizer.lemmatize(word) for word in user_input if word.isalpha()]
    return user_input

# Function to get response
def get_response(user_input):
    user_input = clean_input(user_input)
    bag = []
    for word in user_input:
        for i, w in enumerate(words):
            if word == w:
                bag.append(i)
                break
    if bag:
        output = model.predict(np.array([bag]))
        output = output[0]
        response = np.argmax(output)
        for i, r in enumerate(labels):
            if i == response:
                return random.choice(intents['intents'][r]['responses'])
    return 'I did not understand that.'

# Create GUI
root = tk.Tk()
root.title("Chatbot")

# Create text box for user input
user_input = scrolledtext.ScrolledText(root, width=50, height=5)
user_input.pack(padx=5, pady=5)

# Create text box for chat log
chat_log = scrolledtext.ScrolledText(root, width=50, height=10)
chat_log.pack(padx=5, pady=5)

# Function to handle user input
def handle_input():
    user_input_str = user_input.get('1.0', tk.END)
    response = get_response(user_input_str)
    chat_log.insert(tk.END, 'You: ' + user_input_str + '\n')
    chat_log.insert(tk.END, 'Bot: ' + response + '\n')
    user_input.delete('1.0', tk.END)

# Create button to submit user input
submit_button = tk.Button(root, text='Submit', command=handle_input)
submit_button.pack(padx=5, pady=5)

# Start GUI event loop
root.mainloop()