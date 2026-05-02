import speech_recognition as sr


class SmartHomeController:
    def __init__(self):
        self.devices = {
            "lights": False,
            "thermostat": 22,
            "security": False
        }
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def process_command(self, command: str):
        command = command.lower()

        if "turn on lights" in command:
            self.devices["lights"] = True
            print("Lights turned ON")

        elif "turn off lights" in command:
            self.devices["lights"] = False
            print("Lights turned OFF")

        elif "set thermostat to" in command:
            try:
                value = int(command.split("set thermostat to")[1].strip().split()[0])
                self.devices["thermostat"] = value
                print(f"Thermostat set to {value}°C")
            except:
                print("Could not set thermostat")

        elif "arm security" in command:
            self.devices["security"] = True
            print("Security system ARMED")

        elif "disarm security" in command:
            self.devices["security"] = False
            print("Security system DISARMED")

        elif "status" in command:
            print("Device Status:")
            print(self.devices)

        else:
            print("Command not recognized")

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening for commands...")

            while True:
                try:
                    audio = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {command}")
                    self.process_command(command)

                except sr.UnknownValueError:
                    print("Could not understand audio")

                except sr.RequestError:
                    print("Speech recognition service error")


if __name__ == "__main__":
    controller = SmartHomeController()
    controller.listen()