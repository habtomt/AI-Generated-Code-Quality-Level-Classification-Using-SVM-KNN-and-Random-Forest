"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
from pytube import YouTube
from googletrans import Translator
from gtts import gTTS
import os

def generate_captions(url, language):
    try:
        # Download the video using YouTube API
        yt = YouTube(url)
        
        # Get the video title and description
        title = yt.title
        description = yt.description
        
        # Create a translator object
        translator = Translator()
        
        # Translate the title and description to the desired language
        translated_title = translator.translate(title, dest=language).text
        translated_description = translator.translate(description, dest=language).text
        
        # Create a text-to-speech object
        tts = gTTS(text=translated_description, lang=language)
        
        # Save the audio to a file
        tts.save("description.mp3")
        
        # Create captions file
        captions = f"# Auto-generated captions for {url}\n\n{translated_title}\n\n{translated_description}"
        
        # Save the captions to a file
        with open("captions.txt", "w") as f:
            f.write(captions)
        
        # Print success message
        print("Captions generated successfully!")
        
    except Exception as e:
        # Handle any exceptions
        print(f"Error: {str(e)}")


def main():
    # Test the function with a YouTube URL and language
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    language = "en"
    generate_captions(url, language)


if __name__ == "__main__":
    main()