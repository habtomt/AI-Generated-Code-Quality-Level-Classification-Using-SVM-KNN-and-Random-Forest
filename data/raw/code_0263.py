import pyttsx3
import time
import random

class NavigationAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume', 1.0)
        
        self.route_steps = [
            "In 500 feet, turn right onto Main Street.",
            "Continue straight for 2 miles.",
            "Traffic update: Minor delay ahead, but you are still on the fastest route.",
            "In 200 feet, turn left onto Oak Avenue.",
            "Arriving at your destination on the right."
        ]
        
        self.updates = [
            "Weather update: Light rain expected in 10 minutes.",
            "Point of interest: You are passing the City Library on your left.",
            "Alert: Speed camera reported ahead.",
            "Reminder: Low fuel. There is a gas station 1 mile away."
        ]

    def speak(self, text):
        print(f"[NAV]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def start_navigation(self):
        self.speak("Starting hands-free navigation. Destination set.")
        
        for i, step in enumerate(self.route_steps):
            # Simulate driving time between directions
            time.sleep(2) 
            
            # Provide the direction
            self.speak(step)
            
            # Occasionally provide an informational update between directions
            if i < len(self.route_steps) - 1 and random.choice([True, False]):
                time.sleep(1.5)
                update = random.choice(self.updates)
                self.speak(update)
                
        self.speak("Navigation complete. Have a safe day.")

if __name__ == "__main__":
    # Requirements: pip install pyttsx3
    assistant = NavigationAssistant()
    
    try:
        assistant.start_navigation()
    except KeyboardInterrupt:
        print("\nNavigation terminated.")