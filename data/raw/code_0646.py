"""
Auto-generated Python code
Scenario : Translation
Prompt   : response_000.txt
Run      : 1
"""

import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import playsound
import webbrowser

def listen_and_translate(source_lang='en', target_lang='es'):
    """
    Recognize speech from the microphone, translate it, and then output the translation.
    
    Args:
    source_lang (str): The source language code (e.g., 'en' for English, 'es' for Spanish).
    target_lang (str): The target language code (e.g., 'es' for Spanish, 'fr' for French).
    """
    
    # Validate language codes
    if source_lang not in LANGUAGES and target_lang not in LANGUAGES:
        print("Invalid language code. Please use a valid language code, e.g., 'en' for English or 'es' for Spanish.")
        return
    
    # Initialize speech recognition and translation
    recognizer = sr.Recognizer()
    translator = Translator()
    
    with sr.Microphone() as source:
        print(f"Listening (input language: {source_lang})...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            # Use Google's speech recognition
            text = recognizer.recognize_google(audio, language=source_lang)
            print(f"Recognized: {text}")

            # Translate
            translation = translator.translate(text, src=source_lang, dest=target_lang)
            translated_text = translation.text
            print(f"Translated: {translated_text}")

            # Convert translation text to speech
            tts = gTTS(translated_text, lang=target_lang)
            audio_file = "translation.mp3"
            tts.save(audio_file)

            # Play the translated audio
            playsound.playsound(audio_file)
            
            # Clean up the audio file
            os.remove(audio_file)

            # Open the translated text in the default browser
            open_link = f"https://translate.google.com/#view=home&op=translate&sl={source_lang}&tl={target_lang}&text={text}"
            webbrowser.open_new_tab(open_link)
            
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Customize the source and target languages as needed
    listen_and_translate(source_lang='en', target_lang='es')