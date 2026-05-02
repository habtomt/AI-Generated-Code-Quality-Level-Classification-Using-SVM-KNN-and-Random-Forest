import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
import playsound

def speak(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    filename = tempfile.NamedTemporaryFile(delete=True, suffix=".mp3").name
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def translate_text(text, dest_lang="en"):
    translator = Translator()
    result = translator.translate(text, dest=dest_lang)
    return result.text

def listen_and_translate(source_lang="tr", target_lang="en", audio_output=True):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening... (Press Ctrl+C to stop)")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language=source_lang)
                print(f"Original: {text}")

                translated = translate_text(text, target_lang)
                print(f"Translated: {translated}")

                if audio_output:
                    speak(translated, lang=target_lang)

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError:
                print("Speech recognition service error")
            except KeyboardInterrupt:
                print("Stopped")
                break

if __name__ == "__main__":
    SOURCE_LANG = "tr-TR"
    TARGET_LANG = "en"
    AUDIO_OUTPUT = True

    listen_and_translate(SOURCE_LANG, TARGET_LANG, AUDIO_OUTPUT)