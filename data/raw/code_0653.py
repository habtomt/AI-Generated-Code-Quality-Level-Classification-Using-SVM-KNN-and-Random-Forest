"""
Auto-generated Python code
Scenario : Translation
Prompt   : response_002.txt
Run      : 2
"""

# Required imports
import moviepy.editor as mp
import googletrans
from googletrans.exceptions import TranslateError
from pydub import AudioSegment
import os

# Google Translate API credentials
YOUR_API_KEY = "YOUR_API_KEY"

class SubtitleTranslator:
    def __init__(self, subtitle_path, audio_path, output_path):
        self.subtitle_path = subtitle_path
        self.audio_path = audio_path
        self.output_path = output_path

    def translate_subtitle(self):
        # Load subtitle file
        with open(self.subtitle_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Initialize translated subtitle lines
        translated_lines = []

        # Get audio duration
        audio = AudioSegment.from_file(self.audio_path)
        duration = len(audio) / 1000  # Convert ms to s

        # Initialize current time
        current_time = 0

        # Iterate over each line in the subtitle
        for line in lines:
            # Split line into time and text
            time, text = line.strip().split(' --> ')

            # Convert time to seconds
            start_time, end_time = map(float, time.split('.'))

            # Translate text using Google Translate API
            try:
                translator = googletrans.Translator()
                translation = translator.translate(text, dest='en')  # Translate to English here, change 'en' to the desired language
                translated_text = translation.text
            except TranslateError as e:
                print(f"Error translating text: {e}")
                translated_text = text

            # Calculate duration of current line
            line_duration = end_time - start_time

            # Update current time
            current_time += line_duration

            # Append translated line to list
            translated_lines.append(f"{start_time}.{int((start_time - start_time % 0.1) * 100)} --> {end_time}.{int((end_time - end_time % 0.1) * 100)}\t{translated_text}")

        # Write translated subtitle to file
        with open(self.output_path, 'w', encoding='utf-8') as file:
            file.writelines(translated_lines)

        # Create video with translated subtitle
        video = mp.VideoFileClip(self.audio_path)
        text_clip = mp.TextClip(translated_lines, fontsize=40, color='white')
        text_clip = text_clip.set_position('center').set_duration(duration)
        final_video = mp.CompositeVideoClip([video, text_clip.set_opacity(0.5)])
        final_video.write_videofile(self.output_path.replace('.srt', '.mp4'))

    def run(self):
        try:
            self.translate_subtitle()
        except Exception as e:
            print(f"Error: {e}")

# Example usage
def main():
    subtitle_path = "input.srt"
    audio_path = "input.mp4"
    output_path = "output.srt"
    translator = SubtitleTranslator(subtitle_path, audio_path, output_path)
    translator.run()

if __name__ == "__main__":
    main()