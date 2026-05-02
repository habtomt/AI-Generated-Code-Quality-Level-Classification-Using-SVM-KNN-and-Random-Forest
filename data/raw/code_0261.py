import speech_recognition as sr
import pyttsx3
import sys

class InteractiveCustomerService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 0.9)
        
        self.knowledge_base = {
            "status": "Your order is currently being processed and will ship within 24 hours.",
            "pricing": "Our subscription plans start at $19 per month. You can find details on our website.",
            "support": "You can reach our technical team at support@example.com or stay on the line.",
            "hours": "We are available 24/7 to assist you with your inquiries.",
            "refund": "Refunds are processed within 5 to 7 business days once approved."
        }

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("\nListening for your query...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Customer: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                self.speak("I'm sorry, I didn't quite catch that.")
                return None
            except sr.RequestError:
                self.speak("I'm having trouble connecting to the speech service.")
                return "exit"

    def process_query(self, query):
        if any(word in query for word in ["exit", "bye", "goodbye", "quit"]):
            self.speak("Thank you for contacting us. Have a wonderful day!")
            return False

        found_match = False
        for key, response in self.knowledge_base.items():
            if key in query:
                self.speak(response)
                found_match = True
                break
        
        if not found_match:
            self.speak("I don't have information on that specific topic. Would you like to speak with a representative?")
        
        return True

    def start(self):
        self.speak("Hello! Thank you for calling customer service. How can I help you today?")
        
        active = True
        while active:
            customer_query = self.listen()
            if customer_query:
                active = self.process_query(customer_query)

if __name__ == "__main__":
    # Required: pip install SpeechRecognition pyttsx3 PyAudio
    service = InteractiveCustomerService()
    try:
        service.start()
    except KeyboardInterrupt:
        print("\nSystem offline.")
        sys.exit()