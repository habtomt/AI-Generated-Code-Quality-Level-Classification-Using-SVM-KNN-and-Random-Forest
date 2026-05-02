#!/usr/bin/env python3

import re
import random

def normalize(text):
    return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower()).strip()

def get_response(user_input):
    user_input = normalize(user_input)

    responses = {
        "hello": ["Hello!", "Hi there!", "Hey! How can I help you?"],
        "how are you": ["I'm doing well!", "All good here!", "I'm just code, but I'm fine :)"],
        "what is your name": ["I'm a simple chatbot.", "You can call me PyBot.", "I don't really have a name."],
        "bye": ["Goodbye!", "See you later!", "Bye! Have a great day!"],
    }

    for key in responses:
        if key in user_input:
            return random.choice(responses[key])

    if "help" in user_input:
        return "I'm here to chat! Try saying hello, asking my name, or saying bye."

    return "I didn't quite understand that. Can you rephrase?"

def chat():
    print("ChatBot: Hello! Type 'bye' to exit.")

    while True:
        user_input = input("You: ")

        if normalize(user_input) == "bye":
            print("ChatBot:", random.choice(["Goodbye!", "Bye!", "See you soon!"]))
            break

        response = get_response(user_input)
        print("ChatBot:", response)

if __name__ == "__main__":
    chat()