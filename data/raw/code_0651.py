"""
Auto-generated Python code
Scenario : Translation
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr
from tkinter import Tk
from tkinter import messagebox

# Set up the translator and tts objects
def translate_text(input_text, target_lang):
    try:
        translator = Translator()
        result = translator.translate(input_text, dest=target_lang)
        return result.text
    except Exception as e:
        print(f"Error translating text: {e}")

def text_to_speech(text, target_lang):
    try:
        # Use Google Translate to translate the text to the target language
        translated_text = translate_text(text, target_lang)
        
        # Use gTTS to convert the translated text to speech
        tts = gTTS(text=translated_text, lang=target_lang)
        tts.save("output.mp3")
        
        # Play the audio file
        os.system("start output.mp3")  # For Windows
        # os.system("afplay output.mp3")  # For MacOS
        # os.system("aplay output.mp3")  # For Linux
    except Exception as e:
        print(f"Error converting text to speech: {e}")

def audio_to_text():
    try:
        # Create a Recognizer object
        r = sr.Recognizer()
        
        # Use the microphone as the audio source
        with sr.Microphone() as source:
            # Prompt the user to speak
            print("Please say something:")
            
            # Listen for audio
            audio = r.listen(source)
            
            # Use Google's speech recognition API to transcribe the audio
            try:
                speech_text = r.recognize_google(audio)
                print(f"You said: {speech_text}")
                return speech_text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def main():
    # Create a Tkinter window to handle user input
    root = Tk()
    root.withdraw()  # Hide the window
    
    # Prompt the user for input
    print("Welcome to the language translator!")
    user_input = input("Please enter some text or type 'record' to use the microphone: ")
    
    if user_input.lower() == "record":
        # Get the user's speech input
        user_input = audio_to_text()
    else:
        # Get the user's text input
        user_input = input("Please enter some text: ")
    
    # Prompt the user for the target language
    print("Please select a target language:")
    print("1. English")
    print("2. Spanish")
    print("3. French")
    print("4. German")
    print("5. Italian")
    target_lang_choice = input("Enter the number of your chosen language: ")
    
    if target_lang_choice == "1":
        target_lang = "en"
    elif target_lang_choice == "2":
        target_lang = "es"
    elif target_lang_choice == "3":
        target_lang = "fr"
    elif target_lang_choice == "4":
        target_lang = "de"
    elif target_lang_choice == "5":
        target_lang = "it"
    else:
        print("Invalid language choice. Exiting program.")
        return
    
    # Translate the user's input to the target language
    translated_text = translate_text(user_input, target_lang)
    
    # Provide the translated text or audio output
    print(f"Translated text: {translated_text}")
    tts_choice = input("Would you like the translated text to be spoken? (yes/no): ")
    if tts_choice.lower() == "yes":
        text_to_speech(user_input, target_lang)

if __name__ == "__main__":
    main()