"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_003.txt
Run      : 3
"""

# Import the required library
import googletrans

# Initialize the translator
translator = googletrans.Translator()

def translate_text(text, src_lang, dest_lang):
    """
    Translate text from source language to destination language.

    Args:
        text (str): The text to be translated.
        src_lang (str): The source language code (e.g. en, es, fr, etc.)
        dest_lang (str): The destination language code (e.g. en, es, fr, etc.)

    Returns:
        str: The translated text.
    """
    try:
        # Use the translate function to get the translation
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except googletrans.exceptions.TranslationError as e:
        print(f"Error translating text: {e}")
        return None

def main():
    # Set the source and destination language codes
    src_lang = "en"  # English
    dest_lang = "es"  # Spanish

    # Set the text to be translated
    text = "Hello, how are you?"

    # Call the translate_text function
    translated_text = translate_text(text, src_lang, dest_lang)

    # Print the original and translated text
    if translated_text:
        print(f"Original Text: {text}")
        print(f"Translated Text ({src_lang} to {dest_lang}): {translated_text}")

if __name__ == "__main__":
    main()