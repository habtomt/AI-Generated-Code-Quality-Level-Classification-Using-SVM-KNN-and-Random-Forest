#!/usr/bin/env python3

import pyttsx3
import sys
import time

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def speak(text: str):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

def generate_response(query: str) -> str:
    q = query.lower()

    if any(word in q for word in ["hello", "hi", "hey"]):
        return "Hello! How can I assist you today?"

    if "price" in q:
        return "You can check product prices on our official website or app."

    if "refund" in q:
        return "Refund requests are processed within 3 to 5 business days."

    if "order" in q:
        return "Please provide your order ID so I can check the status."

    if "support" in q:
        return "Our support team is available 24/7 to assist you."

    if "bye" in q or "exit" in q:
        return "Goodbye! Have a great day."

    return "I'm here to help. Could you please clarify your request?"

def main():
    speak("Customer service voice assistant started. How can I help you?")

    while True:
        try:
            query = input("You: ").strip()
            if not query:
                continue

            response = generate_response(query)
            speak(response)

            if "bye" in query.lower() or "exit" in query.lower():
                break

            time.sleep(0.2)

        except KeyboardInterrupt:
            speak("Session ended. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()