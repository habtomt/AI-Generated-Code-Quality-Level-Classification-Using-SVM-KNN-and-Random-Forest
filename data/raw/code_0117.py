#!/usr/bin/env python3

import pyttsx3
import time
import sys

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def speak(text: str):
    print("NAV:", text)
    engine.say(text)
    engine.runAndWait()

def get_route(destination: str):
    return [
        f"Start your journey towards {destination}.",
        "Head straight for 500 meters.",
        "Turn right at the next intersection.",
        "Continue straight for 1 kilometer.",
        "Take the second left turn.",
        f"You have arrived at {destination}."
    ]

def navigation_loop(destination: str):
    route = get_route(destination)

    speak(f"Navigation started to {destination}")

    for step in route:
        speak(step)
        time.sleep(2)

    speak("Navigation completed.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python navigator.py <destination>")
        sys.exit(1)

    destination = " ".join(sys.argv[1:]).strip()

    if not destination:
        print("Please provide a valid destination.")
        sys.exit(1)

    try:
        navigation_loop(destination)
    except KeyboardInterrupt:
        speak("Navigation stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()