import speech_recognition as sr
import pyttsx3

class VoiceSupportSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.faq_database = {
            "shipping": "Standard shipping takes 3 to 5 business days.",
            "refund": "You can request a refund within 30 days of purchase through our website.",
            "password": "To reset your password, click 'Forgot Password' on the login screen.",
            "hours": "We are open from 9 AM to 6 PM, Monday through Friday."
        }

    def speak(self, text):
        print(f"Support: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening for inquiry...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                query = self.recognizer.recognize_google(audio).lower()
                print(f"Customer: {query}")
                return query
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                return None
            except sr.RequestError:
                self.speak("My connection is down. Please try again later.")
                return "exit"

    def route_to_agent(self):
        self.speak("I'm sorry I couldn't help with that. Please stay on the line while I connect you to a human agent.")
        print(">> CALL ROUTED TO HUMAN AGENT <<")

    def run(self):
        self.speak("Hello, I am your automated assistant. How can I help you today?")
        
        while True:
            query = self.listen()
            
            if not query:
                self.speak("I didn't quite catch that. Could you repeat it?")
                continue
            
            if "exit" in query or "goodbye" in query:
                self.speak("Thank you for calling. Goodbye!")
                break
            
            answered = False
            for keyword, response in self.faq_database.items():
                if keyword in query:
                    self.speak(response)
                    self.speak("Does that resolve your issue?")
                    answered = True
                    break
            
            if not answered:
                if "agent" in query or "human" in query or "talk to someone" in query:
                    self.route_to_agent()
                    break
                else:
                    self.speak("I'm not sure about that. Can you rephrase, or would you like to speak to an agent?")

if __name__ == "__main__":
    # Requirements: pip install SpeechRecognition pyttsx3 pyaudio
    support_system = VoiceSupportSystem()
    support_system.run()