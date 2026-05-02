"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_003.txt
Run      : 1
"""

# Required imports at the top
from google.cloud import translate_v2 as translate
import os

# Function to translate text from source language to target language
def translate_text(text, target_language):
    try:
        # Instantiates a client
        translate_client = translate.Client()

        # Translates some text into the target language
        result = translate_client.translate(text, target_lang=target_language)

        print("Text: {}".format(result["input"]))
        print("Translation: {}".format(result["translatedText"]))
        print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    except Exception as e:
        print("Error translating text: {}".format(e))

# Main execution block
if __name__ == "__main__":
    # Set the environment variable for authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/service_account.json'

    text_to_translate = "Hello, how are you?"
    target_language_code = "es"  # Spanish language code

    # Call the function to translate text
    translate_text(text_to_translate, target_language_code)