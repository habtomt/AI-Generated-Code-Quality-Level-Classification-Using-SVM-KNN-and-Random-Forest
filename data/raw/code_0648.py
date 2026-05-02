"""
Auto-generated Python code
Scenario : Translation
Prompt   : response_002.txt
Run      : 1
"""

import pysrt
from googletrans import Translator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def translate_subtitle(input_file, output_file, target_language):
    """
    Translate a subtitle file from one language to another while maintaining accurate timing and context.

    Args:
        input_file (str): Path to the input subtitle file.
        output_file (str): Path to the output subtitle file.
        target_language (str): Language code of the target language (e.g., 'fr' for French).

    Returns:
        None
    """
    # Initialize the translator
    translator = Translator()

    try:
        # Read the input subtitle file
        subs = pysrt.open(input_file)

        # Translate each subtitle entry
        for sub in subs:
            # Translate the subtitle text
            translation = translator.translate(sub.text, dest=target_language).text
            # Update the subtitle text with the translation
            sub.text = translation

        # Write the translated subtitles to the output file
        subs.save(output_file, encoding='utf-8')
        logger.info(f'Translation complete. Output saved to {output_file}')
    except Exception as e:
        logger.error(f'Failed to translate subtitles: {e}')

if __name__ == "__main__":
    # Example usage
    input_srt_file = 'input_subtitles.srt'
    output_srt_file = 'translated_subtitles.srt'
    target_lang = 'fr'  # Example: Translate to French

    translate_subtitle(input_srt_file, output_srt_file, target_lang)