"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_002.txt
Run      : 1
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pyttsx3
import PyPDF2
import io
import os

def get_text_from_website(url):
    # Get the HTML content of the website
    response = requests.get(url)
    response.raise_for_status()  # will raise an error for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text from the HTML
    texts = soup.find_all(text=True)
    visible_texts = filter(tag_visible, texts)

    return " ".join(t.strip() for t in visible_texts)

def tag_visible(element):
    # Filters out tags that should not be read
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_text_from_pdf(pdf_content):
    # Read PDF content
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    text = ''
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text() + '\n'
    return text

def read_aloud(text):
    # Convert text to speech using pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def read_aloud_gtts(text, lang='en'):
    # Convert text to speech using gTTS and play it
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("temp_audio.mp3")
    # Play the audio (requires an audio player installed)
    os.system("start temp_audio.mp3")  # On Windows, use "start", on macOS use "afplay", and on Linux use "mpg123" or "mpg321"

def main():
    print("Choose the option:")
    print("1. Read text from website")
    print("2. Read text from PDF document")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        url = input("Enter the URL of the website: ")
        text = get_text_from_website(url)
    elif choice == '2':
        pdf_path = input("Enter the file path of the PDF: ")
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        text = get_text_from_pdf(pdf_content)
    else:
        print("Invalid choice")
        return

    print("1. Use pyttsx3")
    print("2. Use gTTS")
    tts_choice = input("Choose TTS engine (1/2): ")

    if tts_choice == '1':
        read_aloud(text)
    elif tts_choice == '2':
        read_aloud_gtts(text)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()