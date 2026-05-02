import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

class VirtualAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.reminders = []
        self.schedule = {
            "monday": ["9:00 AM - Team Meeting", "2:00 PM - Code Review"],
            "tuesday": ["11:00 AM - Client Call"],
            "wednesday": ["10:00 AM - Project Planning"],
            "thursday": ["1:00 PM - Development Sprint"],
            "friday": ["4:00 PM - Demo Session"]
        }

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("\nListening...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You: {command}")
                return command
            except Exception:
                return ""

    def handle_command(self, command):
        if "reminder" in command:
            reminder_text = command.replace("set a reminder for", "").replace("set reminder", "").strip()
            self.reminders.append(reminder_text)
            self.speak(f"Okay, I've added '{reminder_text}' to your reminders.")

        elif "search" in command:
            query = command.replace("search for", "").replace("search", "").strip()
            url = f"https://www.google.com/search?q={query}"
            self.speak(f"Searching for {query} on the web.")
            webbrowser.open(url)

        elif "schedule" in command or "calendar" in command:
            day = datetime.datetime.now().strftime("%A").lower()
            today_tasks = self.schedule.get(day, ["No tasks scheduled for today."])
            self.speak(f"For today, {day}, you have:")
            for task in today_tasks:
                self.speak(task)

        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}.")

        elif "stop" in command or "exit" in command:
            self.speak("Goodbye!")
            return False
        
        else:
            self.speak("I'm sorry, I don't know how to do that yet.")
        
        return True

    def start(self):
        self.speak("Hello! I am your virtual assistant. How can I help you today?")
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.handle_command(command)

if __name__ == "__main__":
    # Dependencies: pip install SpeechRecognition pyttsx3 PyAudio
    assistant = VirtualAssistant()
    assistant.start()