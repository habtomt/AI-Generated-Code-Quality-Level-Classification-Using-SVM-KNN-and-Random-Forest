"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
import pyttsx3
import speech_recognition as sr
import datetime
import random

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognition engine
r = sr.Recognizer()

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to audio and recognize speech
def listen_to_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-US")
            print("Customer Query:", query)
            return query
        except sr.UnknownValueError:
            text_to_speech("Sorry, I couldn't understand that. Please try again.")
            return listen_to_speech()
        except sr.RequestError as e:
            text_to_speech("Sorry, there was an error with the request. Please try again.")
            return listen_to_speech()

# Function to provide voice responses
def provide_response(query):
    if query.lower() == "hello":
        text_to_speech("Hello! How can I assist you today?")
    elif query.lower() == "what's your name":
        text_to_speech("My name is Assistant, and I'm here to help you with any questions or concerns.")
    elif query.lower() == "how are you":
        text_to_speech("I'm doing well, thank you for asking! How about you?")
    elif query.lower() == "what time is it":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        text_to_speech(f"The current time is {current_time}.")
    elif query.lower() == "can you tell me a joke":
        jokes = ["Why did the chicken cross the road?", "What do you call a group of cows playing instruments?", "Why did the scarecrow win an award?"]
        joke = random.choice(jokes)
        text_to_speech(joke)
    else:
        text_to_speech("Sorry, I couldn't understand that. Please try again.")

# Main program loop
while True:
    query = listen_to_speech()
    provide_response(query)