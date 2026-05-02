"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_003.txt
Run      : 2
"""

# Import necessary libraries
import googletrans
from googletrans import LANGUAGES, Translator

def translate_text(text, src_lang, dest_lang):
    """
    Translate the given text from source language to destination language.
    
    Args:
    text (str): The text to be translated.
    src_lang (str): The source language code (e.g., 'en' for English).
    dest_lang (str): The destination language code (e.g., 'es' for Spanish).
    
    Returns:
    str: The translated text.
    """
    try:
        # Initialize the translator
        translator = Translator()
        
        # Translate the text
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        
        # Return the translated text
        return result.text
    
    except Exception as e:
        # Handle any exceptions that occur
        print(f"Error: {e}")
        return None

def get_language_names():
    """
    Get the list of supported languages with their names.
    
    Returns:
    dict: A dictionary where keys are language codes and values are language names.
    """
    try:
        # Get the list of supported languages with their names
        languages = LANGUAGES
        
        # Return the dictionary of language names
        return languages
    
    except Exception as e:
        # Handle any exceptions that occur
        print(f"Error: {e}")
        return None

def main():
    # Placeholder source and destination language codes
    src_lang = 'en'
    dest_lang = 'es'
    
    # Text to be translated
    text = "Hello, how are you?"
    
    # Print the language names
    print("Supported Languages:")
    languages = get_language_names()
    for code, name in languages.items():
        print(f"{code}: {name}")
    
    # Translate the text
    translated_text = translate_text(text, src_lang, dest_lang)
    
    # Print the translated text
    if translated_text is not None:
        print(f"Translated Text ({src_lang} -> {dest_lang}):")
        print(translated_text)

if __name__ == "__main__":
    main()