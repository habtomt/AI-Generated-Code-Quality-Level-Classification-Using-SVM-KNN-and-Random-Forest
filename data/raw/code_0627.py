"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import speech_recognition as sr
import pyaudio
import vosk
import json
import os
import datetime

# Set up Vosk model path
model_path = 'vosk-model-small-en-us-0.15'

# Initialize Vosk model
vosk.setLogLevel(-1)
model = vosk.Model(model_path)

# Initialize Speech Recognition object
r = sr.Recognizer()

# Function to transcribe audio from a file
def transcribe_file(file_path):
    try:
        # Open audio file
        with sr.AudioFile(file_path) as source:
            # Read audio data
            audio = r.record(source)
            # Transcribe audio
            transcription = vosk.KaldiRecognizer(model, r.sample_rate, 0.0)
            transcription_result = None
            if audio.data != b"" and transcription.AcceptWaveform(audio.get_raw_data(), audio.sample_rate):
                transcription_result = transcription.Result()
            elif audio.data != b"" and transcription.PartialResult():
                transcription_result = transcription.PartialResult()
            elif transcription.FinalResult():
                transcription_result = transcription.FinalResult()
            else:
                transcription_result = "No speech detected"
            return transcription_result
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return "Error requesting results from speech recognition service: {0}".format(e)

# Function to save transcription to a JSON file
def save_transcription(file_path, transcription):
    with open(file_path, 'w') as f:
        json.dump(transcription, f)

# Function to record audio from the microphone
def record_audio():
    print("Recording...")
    r.listen(source)
    print("Recording finished")

# Main function
def main():
    # Set up audio input
    source = sr.Microphone()

    # Set up Vosk model
    vosk_model = vosk.Model(model_path)

    # Ask user for file name
    file_name = input("Enter file name: ")

    # Record audio
    print("Press Ctrl+C to stop recording")
    try:
        # Record audio into a file
        with open(file_name + '.wav', 'wb') as f:
            print("Recording audio into file...")
            r.listen(source, phrase_time_limit=10)
            print("Recording finished")
            f.write(source.record(duration=10).get_raw_data())
    except KeyboardInterrupt:
        print("Recording stopped")

    # Transcribe audio from file
    transcription = transcribe_file(file_name + '.wav')

    # Save transcription to file
    save_transcription(file_name + '.json', transcription)

    # Print transcription to console
    print(transcription)

if __name__ == "__main__":
    main()