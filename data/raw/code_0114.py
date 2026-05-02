#!/usr/bin/env python3

import sys
import pyttsx3

def load_content(source: str) -> str:
    try:
        with open(source, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return source

def speak_text(text: str):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()

def main():
    if len(sys.argv) < 2:
        print("Usage: python tts.py '<text_or_file_path>'")
        sys.exit(1)

    input_data = sys.argv[1]
    content = load_content(input_data)

    if not content.strip():
        print("No content to read.")
        sys.exit(1)

    speak_text(content)

if __name__ == "__main__":
    main()