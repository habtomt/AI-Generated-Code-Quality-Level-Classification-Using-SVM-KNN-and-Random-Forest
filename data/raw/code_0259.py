import moviepy.editor as mp
import speech_recognition as sr
from datetime import timedelta
import os

class VideoCaptioner:
    def __init__(self, video_path):
        self.video_path = video_path
        self.audio_path = "temp_audio.wav"
        self.recognizer = sr.Recognizer()

    def extract_audio(self):
        video = mp.VideoFileClip(self.video_path)
        video.audio.write_audiofile(self.audio_path, codec='pcm_s16le')

    def format_timestamp(self, seconds):
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        millis = int(td.microseconds / 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

    def generate_srt(self, output_srt="captions.srt", segment_duration=10):
        self.extract_audio()
        
        audio_clip = mp.AudioFileClip(self.audio_path)
        duration = int(audio_clip.duration)
        
        with open(output_srt, "w", encoding="utf-8") as srt_file:
            counter = 1
            for start in range(0, duration, segment_duration):
                end = min(start + segment_duration, duration)
                
                with sr.AudioFile(self.audio_path) as source:
                    audio_segment = self.recognizer.record(source, offset=start, duration=segment_duration)
                    
                try:
                    text = self.recognizer.recognize_google(audio_segment)
                    
                    start_time = self.format_timestamp(start)
                    end_time = self.format_timestamp(end)
                    
                    srt_file.write(f"{counter}\n")
                    srt_file.write(f"{start_time} --> {end_time}\n")
                    srt_file.write(f"{text}\n\n")
                    
                    print(f"Processed: {start_time} -> {text}")
                    counter += 1
                except (sr.UnknownValueError, sr.RequestError):
                    continue

        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)
        
        print(f"\nSuccess: Captions saved to {output_srt}")

if __name__ == "__main__":
    # Requirements: pip install moviepy SpeechRecognition
    # Note: Ensure FFmpeg is installed on your system
    VIDEO_FILE = "input_video.mp4" 
    
    if os.path.exists(VIDEO_FILE):
        captioner = VideoCaptioner(VIDEO_FILE)
        captioner.generate_srt()
    else:
        print(f"File {VIDEO_FILE} not found. Please provide a valid video path.")