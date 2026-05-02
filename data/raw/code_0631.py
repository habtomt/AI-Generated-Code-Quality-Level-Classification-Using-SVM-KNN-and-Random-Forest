"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_000.txt
Run      : 1
"""

# Import the necessary library
from gtts import gTTS
import os

def text_to_speech(text, output_file):
    """
    Convert text to speech and save it as an audio file.
    
    :param text: The text content to convert to speech.
    :param output_file: The file name for the resulting audio file (with .mp3 extension).
    """
    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save the converted audio to a file
        tts.save(output_file)
        
        print(f"Audio content saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Sample educational content
    educational_content = """
    The water cycle is the process by which water circulates between the Earth's oceans,
    atmosphere, and land, involving precipitation as rain and snow, drainage in streams and rivers,
    and return to the atmosphere by evaporation and transpiration.
    
    The water cycle also includes the movement of water through the atmosphere, including evaporation,
    condensation, and precipitation.
    
    This process is essential for life on Earth and is driven by solar energy.
    """
    
    # Convert the text to speech
    text_to_speech(educational_content, "educational_content.mp3")
    
    # Additional example of converting text to speech for different languages
    french_content = "La fontaine de jouvence est un mythe grec qui décrit une source qui fait la jeunesse perpétuelle."
    text_to_speech(french_content, "french_content.mp3")
    
    # Another example of converting text to speech with a different language
    spanish_content = "El ciclo del agua es el proceso por el cual el agua circula entre los océanos, la atmósfera y la tierra, involucrando la precipitación como lluvia y nieve, la drenaje en arroyos y ríos, y el retorno a la atmósfera mediante evaporación y transpiración."
    text_to_speech(spanish_content, "spanish_content.mp3")