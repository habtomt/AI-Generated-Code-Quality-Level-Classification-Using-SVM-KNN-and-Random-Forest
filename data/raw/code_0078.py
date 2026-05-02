#!/usr/bin/env python3

import sys

try:
    from googletrans import Translator
except ImportError:
    print("Missing dependency: googletrans. Install with 'pip install googletrans==4.0.0-rc1'")
    sys.exit(1)

def translate_text(text, dest_lang="en"):
    translator = Translator()
    result = translator.translate(text, dest=dest_lang)
    return result.text

def main():
    if len(sys.argv) < 2:
        text = input("Enter text to translate: ")
        dest_lang = input("Enter target language code (e.g. en, tr, fr): ") or "en"
    else:
        text = sys.argv[1]
        dest_lang = sys.argv[2] if len(sys.argv) > 2 else "en"

    translated = translate_text(text, dest_lang)
    print(translated)

if __name__ == "__main__":
    main()