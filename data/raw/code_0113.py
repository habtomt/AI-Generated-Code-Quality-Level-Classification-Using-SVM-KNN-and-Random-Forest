import sys
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr


def extract_audio(video_path, audio_path="temp_audio.wav"):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, fps=16000, codec="pcm_s16le")
    return audio_path


def format_timestamp(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    hrs = s // 3600
    mins = (s % 3600) // 60
    secs = s % 60
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"


def transcribe(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        duration = source.DURATION
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    except sr.RequestError:
        text = ""

    return text, duration


def generate_srt(text, duration, output_path="output.srt"):
    start = 0
    end = duration

    srt_content = []
    srt_content.append("1")
    srt_content.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
    srt_content.append(text if text else "[Unrecognized Speech]")
    srt_content.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python caption_generator.py <video_file>")
        sys.exit(1)

    video_path = sys.argv[1]

    if not os.path.exists(video_path):
        print("File not found")
        sys.exit(1)

    audio_path = extract_audio(video_path)
    text, duration = transcribe(audio_path)
    output_file = generate_srt(text, duration)

    print(f"Captions generated: {output_file}")

    if os.path.exists(audio_path):
        os.remove(audio_path)


if __name__ == "__main__":
    main()