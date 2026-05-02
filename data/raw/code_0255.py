import speech_recognition as sr

class SmartHomeSystem:
    def __init__(self):
        self.devices = {
            "light": "OFF",
            "thermostat": 72,
            "security": "ARMED"
        }

    def process_command(self, command):
        command = command.lower()
        
        # Light Logic
        if "light" in command:
            if "on" in command:
                self.devices["light"] = "ON"
                print(">> Lights turned ON.")
            elif "off" in command:
                self.devices["light"] = "OFF"
                print(">> Lights turned OFF.")

        # Thermostat Logic
        elif "thermostat" in command:
            words = command.split()
            for word in words:
                if word.isdigit():
                    self.devices["thermostat"] = int(word)
                    print(f">> Thermostat set to {word} degrees.")
                    break

        # Security Logic
        elif "security" in command or "alarm" in command:
            if "disarm" in command:
                self.devices["security"] = "DISARMED"
                print(">> Security system DISARMED.")
            elif "arm" in command:
                self.devices["security"] = "ARMED"
                print(">> Security system ARMED.")
        
        else:
            print(">> Command not recognized. Please try again.")

def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    home = SmartHomeSystem()

    print("--- Smart Home Voice Controller ---")
    print("Commands: 'Turn light on/off', 'Set thermostat to 75', 'Arm/Disarm security'")
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("\nListening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                
                if "exit" in text.lower() or "stop" in text.lower():
                    print("Shutting down...")
                    break
                    
                home.process_command(text)
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Service error: {e}")
                break

if __name__ == "__main__":
    # Note: Requires 'SpeechRecognition' and 'PyAudio' libraries
    listen_for_commands()