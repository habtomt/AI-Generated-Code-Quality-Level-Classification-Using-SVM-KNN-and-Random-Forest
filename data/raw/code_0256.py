import speech_recognition as sr
import datetime
import os

class MeetingTranscriber:
    def __init__(self, output_file="meeting_minutes.txt"):
        self.output_file = output_file
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def record_and_transcribe(self):
        print("--- Meeting Transcription Tool ---")
        print("Type 'STOP' to end recording and save.")
        
        with open(self.output_file, "a") as f:
            f.write(f"\n--- Session Start: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while True:
                    print("Listening...")
                    try:
                        audio = self.recognizer.listen(source, phrase_time_limit=10)
                        text = self.recognizer.recognize_google(audio)
                        
                        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
                        entry = f"{timestamp} {text}\n"
                        
                        print(f"Logged: {text}")
                        
                        with open(self.output_file, "a") as f:
                            f.write(entry)
                            
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        print(f"API Error: {e}")
                        break
                        
        except KeyboardInterrupt:
            print("\nTranscription stopped by user.")
        
        with open(self.output_file, "a") as f:
            f.write(f"--- Session End: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        
        print(f"Full transcript saved to: {os.path.abspath(self.output_file)}")

    def search_transcript(self, keyword):
        if not os.path.exists(self.output_file):
            print("No transcript file found.")
            return

        print(f"\nSearching for: '{keyword}'")
        found = False
        with open(self.output_file, "r") as f:
            for line in f:
                if keyword.lower() in line.lower():
                    print(line.strip())
                    found = True
        
        if not found:
            print("No matches found.")

if __name__ == "__main__":
    # Note: Requires 'SpeechRecognition' and 'PyAudio' libraries
    # Usage: 
    # 1. Run script to record
    # 2. Use 'ctrl+c' to stop and save
    
    transcriber = MeetingTranscriber()
    transcriber.record_and_transcribe()
    
    # Example Search functionality
    # transcriber.search_transcript("decision")