#!/usr/bin/env python3

import pyttsx3
import sys

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def speak(text: str):
    print(text)
    engine.say(text)
    engine.runAndWait()

def choose(prompt, options):
    speak(prompt)
    for i, opt in enumerate(options, 1):
        speak(f"Option {i}: {opt}")

    while True:
        try:
            choice = input("Choose option number: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
        except:
            pass
        speak("Invalid choice, try again.")

def story():
    speak("Welcome to the interactive story experience.")

    speak("You wake up in a dark forest. Two paths lie ahead.")

    choice1 = choose(
        "What do you do?",
        ["Take the left path toward the mountains", "Take the right path into the dense forest"]
    )

    if choice1 == 0:
        speak("You walk toward the mountains and find a glowing cave.")
        choice2 = choose(
            "Do you enter the cave?",
            ["Yes, enter the cave", "No, turn back"]
        )

        if choice2 == 0:
            speak("Inside the cave, you discover a hidden treasure. You win the adventure!")
        else:
            speak("You turn back safely but miss the treasure. The journey ends.")

    else:
        speak("You enter the dense forest and hear strange sounds.")

        choice2 = choose(
            "A shadow approaches. What do you do?",
            ["Run away", "Investigate the shadow"]
        )

        if choice2 == 0:
            speak("You escape safely but remain lost in the forest. The end.")
        else:
            speak("The shadow is a friendly guide who helps you escape. You survive the adventure!")

    speak("Thank you for playing the interactive story.")

def main():
    try:
        story()
    except KeyboardInterrupt:
        speak("Story interrupted. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()