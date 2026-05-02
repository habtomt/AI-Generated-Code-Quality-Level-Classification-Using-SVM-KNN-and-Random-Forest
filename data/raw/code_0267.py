import pysrt
from googletrans import Translator
import time

class SubtitleTranslator:
    def __init__(self, target_lang='es'):
        self.translator = Translator()
        self.target_lang = target_lang

    def translate_file(self, input_file, output_file):
        """Translates an SRT file while maintaining timestamps."""
        try:
            subs = pysrt.open(input_file)
            total_subs = len(subs)
            print(f"Loaded {total_subs} subtitles. Starting translation...")

            for i, sub in enumerate(subs):
                # Clean text of HTML tags often found in subtitles
                original_text = sub.text_without_tags
                
                if original_text.strip():
                    try:
                        translation = self.translator.translate(
                            original_text, 
                            dest=self.target_lang
                        )
                        sub.text = translation.text
                    except Exception as e:
                        print(f"Error at index {i}: {e}")
                        # Maintain original text if translation fails
                        pass

                # Progress update
                if (i + 1) % 10 == 0 or (i + 1) == total_subs:
                    print(f"Progress: {i + 1}/{total_subs} translated...")
                
                # Small sleep to prevent rate limiting from free API
                time.sleep(0.2)

            subs.save(output_file, encoding='utf-8')
            print(f"Success! Translated subtitles saved to: {output_file}")

        except FileNotFoundError:
            print("Error: The input subtitle file was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Requirements: pip install pysrt googletrans==4.0.0-rc1
    
    # Configuration
    INPUT_SRT = "movie_english.srt"  # Path to your source file
    OUTPUT_SRT = "movie_translated.srt"
    TARGET_LANGUAGE = "fr"  # 'es' for Spanish, 'fr' for French, 'de' for German, etc.

    # Create a dummy SRT for execution if one doesn't exist
    import os
    if not os.path.exists(INPUT_SRT):
        with open(INPUT_SRT, "w", encoding="utf-8") as f:
            f.write("1\n00:00:01,000 --> 00:00:04,000\nHello, welcome to the movie.\n\n")
            f.write("2\n00:00:05,000 --> 00:00:08,000\nI hope you enjoy the show.")

    translator_tool = SubtitleTranslator(target_lang=TARGET_LANGUAGE)
    translator_tool.translate_file(INPUT_SRT, OUTPUT_SRT)