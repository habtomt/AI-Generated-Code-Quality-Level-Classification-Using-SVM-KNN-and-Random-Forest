import pyttsx3
import os

class EducationToSpeech:
    def __init__(self, rate=150, volume=1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def list_voices(self):
        voices = self.engine.getProperty('voices')
        for index, voice in enumerate(voices):
            print(f"{index}: {voice.name} ({voice.languages})")

    def set_voice(self, index):
        voices = self.engine.getProperty('voices')
        if 0 <= index < len(voices):
            self.engine.setProperty('voice', voices[index].id)

    def convert_text_to_audio(self, text, filename="lesson_audio.mp3"):
        print(f"Converting content to {filename}...")
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        print("Conversion complete.")

    def read_aloud(self, text):
        print("Reading content aloud...")
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    # Example educational content
    educational_content = """
    Welcome to the Python Programming Lesson. 
    Python is a high-level, interpreted programming language known for its readability.
    Today's key concept is 'Variables'. Variables are used to store information 
    to be referenced and manipulated in a computer program. 
    They provide a way of labeling data with a descriptive name.
    """

    converter = EducationToSpeech(rate=175)
    
    # Optional: Select a specific voice index (usually 0 for male, 1 for female)
    # converter.set_voice(1)

    # Action 1: Play audio directly
    converter.read_aloud(educational_content)

    # Action 2: Save to a file for offline learning
    output_file = "python_lesson_1.mp3"
    converter.convert_text_to_audio(educational_content, output_file)