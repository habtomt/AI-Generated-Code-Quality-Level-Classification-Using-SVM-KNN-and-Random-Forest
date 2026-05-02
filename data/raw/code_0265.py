import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import playsound

class InstantTranslator:
    def __init__(self, target_lang='es'):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.target_lang = target_lang
        self.temp_file = "translation.mp3"

    def speak(self, text, lang):
        """Converts text to speech and plays it."""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(self.temp_file)
            playsound.playsound(self.temp_file)
            os.remove(self.temp_file)
        except Exception as e:
            print(f"Audio Error: {e}")

    def translate_voice(self):
        """Listens to input, translates it, and provides audio/text output."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"\n--- Ready! Speak now (Target Language: {self.target_lang}) ---")
            
            try:
                # Capture the audio
                audio = self.recognizer.listen(source, timeout=5)
                print("Processing speech...")
                
                # Speech to Text (Source Language)
                original_text = self.recognizer.recognize_google(audio)
                print(f"Input: {original_text}")

                # Translation
                translation = self.translator.translate(original_text, dest=self.target_lang)
                translated_text = translation.text
                print(f"Translation: {translated_text}")

                # Text to Speech (Target Language)
                self.speak(translated_text, self.target_lang)

            except sr.WaitTimeoutError:
                print("Listening timed out.")
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Requirements: pip install SpeechRecognition googletrans==4.0.0-rc1 gTTS playsound==1.2.2 PyAudio
    # Note: Use a specific version of googletrans (4.0.0rc1) for better stability.
    
    # Initialize with 'es' for Spanish, 'fr' for French, 'de' for German, etc.
    app = InstantTranslator(target_lang='fr')
    
    while True:
        app.translate_voice()
        user_input = input("\nPress Enter to translate again or 'q' to quit: ").lower()
        if user_input == 'q':
            break