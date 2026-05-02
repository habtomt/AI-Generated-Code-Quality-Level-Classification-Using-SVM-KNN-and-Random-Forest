import pyttsx3
import requests
from bs4 import BeautifulSoup
import os

class AccessibilityReader:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.engine.setProperty('volume', 1.0)

    def speak(self, text):
        if not text.strip():
            print("No text found to read.")
            return
        print(f"Reading: {text[:100]}...")
        self.engine.say(text)
        self.engine.runAndWait()

    def read_from_website(self, url):
        try:
            print(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            content = "\n".join([p.get_text() for p in paragraphs])
            
            self.speak(content)
        except Exception as e:
            print(f"Error accessing website: {e}")

    def read_from_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                print("File not found.")
                return

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.speak(content)
        except Exception as e:
            print(f"Error reading file: {e}")

if __name__ == "__main__":
    # Requirements: pip install pyttsx3 requests beautifulsoup4
    reader = AccessibilityReader()

    # Choice 1: Read a website
    # reader.read_from_website("https://en.wikipedia.org/wiki/Web_accessibility")

    # Choice 2: Read a local document
    # Create a dummy file for demonstration
    temp_doc = "demo_document.txt"
    with open(temp_doc, "w") as f:
        f.write("This is a document designed to assist users with visual impairments. "
                "The system converts written text into audible speech for better accessibility.")
    
    reader.read_from_file(temp_doc)