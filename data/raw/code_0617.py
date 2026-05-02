"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_001.txt
Run      : 1
"""

import pyaudio
import wave
import speech_recognition as sr
import sqlite3
from tkinter import Tk
from tkinter import filedialog
import os

# Parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize pyaudio
audio = pyaudio.PyAudio()

# Function to record audio
def record_audio():
    print("Start recording...")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recording to a file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

# Function to transcribe audio
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio_data = recognizer.record(source)
        try:
            # Use Google's speech recognition
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None

# Function to save transcription to database
def save_transcription(text):
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transcriptions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)''')
    c.execute("INSERT INTO transcriptions (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

# Function to search transcriptions in database
def search_transcriptions(query):
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("SELECT text FROM transcriptions WHERE text LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    return results

# Tkinter GUI
root = Tk()
root.withdraw()

# Open file dialog to select recording location
file_path = filedialog.askdirectory()
if file_path:
    # Record audio
    record_audio()

    # Transcribe audio
    text = transcribe_audio()
    if text:
        # Save transcription to database
        save_transcription(text)

        # Search transcriptions in database
        query = input("Enter search query: ")
        results = search_transcriptions(query)
        for result in results:
            print(result[0])

# Clean up
os.remove(WAVE_OUTPUT_FILENAME)

print("Transcription tool finished.")