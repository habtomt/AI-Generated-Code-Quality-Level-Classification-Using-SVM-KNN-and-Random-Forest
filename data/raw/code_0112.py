import speech_recognition as sr
import pyttsx3
from datetime import datetime, timedelta
import time
import threading


class VirtualAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts = pyttsx3.init()

        self.reminders = []

    def speak(self, text):
        print("ASSISTANT:", text)
        self.tts.say(text)
        self.tts.runAndWait()

    def set_reminder(self, seconds, message):
        remind_time = datetime.now() + timedelta(seconds=seconds)
        self.reminders.append((remind_time, message))
        self.speak(f"Reminder set for {seconds} seconds from now.")

    def check_reminders(self):
        while True:
            now = datetime.now()
            for reminder in self.reminders[:]:
                if now >= reminder[0]:
                    self.speak(f"Reminder: {reminder[1]}")
                    self.reminders.remove(reminder)
            time.sleep(1)

    def search_info(self, query):
        response = f"Search feature is not connected to the internet. You asked about {query}."
        self.speak(response)

    def process_command(self, command):
        command = command.lower()

        if "set reminder" in command:
            try:
                parts = command.split("for")
                seconds = int(parts[1].strip().split()[0])
                message = parts[1].replace(str(seconds), "").strip()
                self.set_reminder(seconds, message)
            except:
                self.speak("Could not set reminder. Please say format: set reminder for 10 seconds take break")

        elif "search" in command:
            query = command.replace("search", "").strip()
            self.search_info(query)

        elif "schedule" in command:
            self.speak("You can manage your schedule in the calendar app.")

        elif "time" in command:
            self.speak(f"The current time is {datetime.now().strftime('%H:%M:%S')}")

        else:
            self.speak("Command not recognized")

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.speak("Virtual assistant is now active")

            while True:
                try:
                    audio = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio)
                    print("USER:", command)
                    self.process_command(command)

                except sr.UnknownValueError:
                    self.speak("I could not understand that")

                except sr.RequestError:
                    self.speak("Speech service error")


if __name__ == "__main__":
    assistant = VirtualAssistant()

    reminder_thread = threading.Thread(target=assistant.check_reminders, daemon=True)
    reminder_thread.start()

    assistant.listen()