"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_004.txt
Run      : 1
"""

from pydub import AudioSegment
import speech_recognition as sr
import os
from datetime import timedelta
import googletrans
from pydub.utils import make_chunks

def extract_audio(video_file, output_format="wav"):
    # Extract audio from video
    audio_output = "audio." + output_format
    AudioSegment.from_file(video_file).export(audio_output, format=output_format)
    return audio_output

def transcribe_audio(audio_file):
    # Transcribe audio to text using Speech Recognition
    recognizer = sr.Recognizer()
    audio_transcript = []

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            audio_transcript.append((0, text))  # Start time set to 0 for simplicity
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    return audio_transcript

def translate_text(text, target_language):
    # Translate text to target language using Google Translate API
    translator = googletrans.Translator()
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

def save_as_srt(transcripts, srt_filename):
    # Save transcripts as SRT file
    with open(srt_filename, 'w') as srt_file:
        for i, (start_time, text) in enumerate(transcripts):
            srt_file.write(f"{i+1}
")
            start_time_str = str(timedelta(seconds=start_time))
            end_time_str = str(timedelta(seconds=start_time + 2))  # assuming each caption lasts 2 seconds
            srt_file.write(f"{start_time_str} --> {end_time_str}
")
            srt_file.write(f"{text}

")

def split_audio_into_chunks(audio_file, chunk_duration=2):
    # Split audio into chunks of specified duration
    audio = AudioSegment.from_file(audio_file)
    chunks = make_chunks(audio, chunk_duration * 1000)  # 1000 ms = 1 s
    return chunks

def transcribe_audio_chunks(audio_chunks):
    # Transcribe each audio chunk to text
    audio_transcript = []
    for i, chunk in enumerate(audio_chunks):
        chunk_audio_file = f"chunk_{i}.wav"
        chunk.export(chunk_audio_file, format="wav")
        chunk_transcript = transcribe_audio(chunk_audio_file)
        audio_transcript.extend(chunk_transcript)
    return audio_transcript

def main():
    video_input = "input_video.mp4"
    audio_file = extract_audio(video_input)
    audio_chunks = split_audio_into_chunks(audio_file)
    transcription = transcribe_audio_chunks(audio_chunks)
    if transcription:
        save_as_srt(transcription, "output.srt")
    else:
        print("No transcriptions available.")

if __name__ == "__main__":
    main()