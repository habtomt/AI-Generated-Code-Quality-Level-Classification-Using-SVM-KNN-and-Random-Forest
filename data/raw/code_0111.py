import speech_recognition as sr
import pyttsx3


class VoiceSupportSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts = pyttsx3.init()

        self.knowledge_base = {
            "reset password": "To reset your password, go to settings and click 'Forgot Password'.",
            "account balance": "Your account balance can be checked in the billing section of the app.",
            "open hours": "Our support is available 24/7."
        }

        self.complex_keywords = ["complaint", "fraud", "legal", "lawsuit", "charge dispute"]

    def speak(self, text):
        print("BOT:", text)
        self.tts.say(text)
        self.tts.runAndWait()

    def route_to_human(self):
        msg = "This issue is complex. Routing you to a human agent now."
        self.speak(msg)
        print("SYSTEM: Routed to human agent.")

    def process_query(self, query):
        query = query.lower()

        if any(word in query for word in self.complex_keywords):
            self.route_to_human()
            return

        for key in self.knowledge_base:
            if key in query:
                self.speak(self.knowledge_base[key])
                return

        self.speak("I'm not sure about that. Connecting you to a human agent.")
        self.route_to_human()

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.speak("Voice support system is now active.")

            while True:
                try:
                    audio = self.recognizer.listen(source)
                    query = self.recognizer.recognize_google(audio)
                    print("USER:", query)
                    self.process_query(query)

                except sr.UnknownValueError:
                    self.speak("Sorry, I couldn't understand that.")

                except sr.RequestError:
                    self.speak("Speech service is unavailable.")


if __name__ == "__main__":
    system = VoiceSupportSystem()
    system.listen()