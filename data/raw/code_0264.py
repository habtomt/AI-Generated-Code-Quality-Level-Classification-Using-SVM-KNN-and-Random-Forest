import pyttsx3
import speech_recognition as sr
import time

class InteractiveStoryteller:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.engine.setProperty('rate', 160)
        
        self.story_tree = {
            "start": {
                "text": "You stand at the edge of a whispering forest. To your left is a narrow path overgrown with thorns. To your right, a stone bridge crosses a rushing river. Do you go left or right?",
                "choices": {"left": "thorns", "right": "bridge"}
            },
            "thorns": {
                "text": "The thorns scratch at your armor, but you find a hidden glowing pendant on the ground. Do you pick it up or leave it?",
                "choices": {"pick": "pendant", "leave": "forest_deep"}
            },
            "bridge": {
                "text": "The bridge creaks under your weight. A grumpy troll pops up and demands a riddle. Do you fight the troll or tell a riddle?",
                "choices": {"fight": "troll_fight", "tell": "riddle_win"}
            },
            "pendant": {
                "text": "The pendant glows brightly, illuminating a path to a hidden treasure room. You have won!",
                "choices": {}
            },
            "riddle_win": {
                "text": "The troll laughs and lets you pass. You find a peaceful village on the other side. The end.",
                "choices": {}
            }
        }

    def speak(self, text):
        print(f"Narrator: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_for_choice(self, valid_choices):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening for your choice...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                choice = self.recognizer.recognize_google(audio).lower()
                print(f"User: {choice}")
                
                for key in valid_choices:
                    if key in choice:
                        return key
                return None
            except:
                return None

    def play(self):
        current_node = "start"
        self.speak("Welcome to the interactive adventure.")
        
        while True:
            node_data = self.story_tree[current_node]
            self.speak(node_data["text"])
            
            if not node_data["choices"]:
                break
            
            while True:
                user_choice = self.listen_for_choice(node_data["choices"].keys())
                if user_choice:
                    current_node = node_data["choices"][user_choice]
                    break
                else:
                    self.speak("I didn't understand. Please choose one of the options mentioned.")

if __name__ == "__main__":
    # Requirements: pip install pyttsx3 SpeechRecognition PyAudio
    game = InteractiveStoryteller()
    game.play()