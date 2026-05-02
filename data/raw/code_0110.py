import speech_recognition as sr
from datetime import datetime


class MeetingTranscriber:
    def __init__(self, output_file="meeting_transcript.txt"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.output_file = output_file

        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write("\n\n--- New Session Started: {} ---\n".format(datetime.now()))

    def transcribe(self, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {text}\n"

        print(line.strip())

        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(line)

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening for meeting audio...")

            while True:
                try:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio)
                    self.transcribe(text)

                except sr.UnknownValueError:
                    print("Could not understand audio")

                except sr.RequestError:
                    print("Speech recognition service unavailable")


if __name__ == "__main__":
    transcriber = MeetingTranscriber()
    transcriber.listen()