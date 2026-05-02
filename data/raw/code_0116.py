#!/usr/bin/env python3

import sys
import requests
import pyttsx3
from bs4 import BeautifulSoup

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

def read_from_url(url: str) -> str:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text(separator=" ")
    lines = [line.strip() for line in text.splitlines()]
    return " ".join([chunk for line in lines for chunk in line.split(" ") if chunk])

def read_from_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: python reader.py <url_or_file_path>")
        sys.exit(1)

    source = sys.argv[1]

    try:
        if source.startswith("http://") or source.startswith("https://"):
            content = read_from_url(source)
        else:
            content = read_from_file(source)

        if not content.strip():
            print("No readable content found.")
            sys.exit(1)

        speak(content)

    except Exception as e:
        print("Error:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()