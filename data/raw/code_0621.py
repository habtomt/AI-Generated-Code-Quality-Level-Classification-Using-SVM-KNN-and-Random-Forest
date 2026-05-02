"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_000.txt
Run      : 2
"""

import speech_recognition as sr
import os
import requests
import json

# Smart Home Device API Endpoints
SMART_HOME_API_URL = "https://YOUR_SMART_HOME_API_URL.com/api/"
API_KEY = "YOUR_API_KEY"

# Recognizer and Microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Device Control Functions
def control_light(command):
    try:
        # Send request to turn light on/off
        response = requests.post(SMART_HOME_API_URL + "lights/switch", headers={"Authorization": f"Bearer {API_KEY}"}, json={"state": command.lower() == "on"})
        # Check if request was successful
        if response.status_code == 200:
            print(f"Light {command} successfully")
        else:
            print("Failed to control light")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def control_thermostat(command):
    try:
        # Send request to set temperature
        temperature = None
        if "set" in command:
            temperature = int(command.split(" ")[1])
        response = requests.post(SMART_HOME_API_URL + "thermostat/set", headers={"Authorization": f"Bearer {API_KEY}"}, json={"temperature": temperature})
        # Check if request was successful
        if response.status_code == 200:
            print(f"Temperature set to {temperature}°C")
        else:
            print("Failed to set temperature")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def control_security(command):
    try:
        # Send request to arm/disarm security system
        response = requests.post(SMART_HOME_API_URL + "security/switch", headers={"Authorization": f"Bearer {API_KEY}"}, json={"state": command.lower() == "arm"})
        # Check if request was successful
        if response.status_code == 200:
            print(f"Security system {command} successfully")
        else:
            print("Failed to control security system")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Main Loop
while True:
    try:
        # Listen for voice command
        with microphone as source:
            print("Listening for voice command...")
            audio = recognizer.listen(source, phrase_time_limit=5)
            try:
                # Attempt to recognize spoken instructions
                command = recognizer.recognize_google(audio, language="en-US")
                print(f"Recognized command: {command}")
                
                # Control devices based on voice command
                if "turn on" in command:
                    control_light(command)
                elif "turn off" in command:
                    control_light(command)
                elif "set temperature" in command:
                    control_thermostat(command)
                elif "arm" in command:
                    control_security(command)
                elif "disarm" in command:
                    control_security(command)
                else:
                    print("Unknown command")
            except sr.UnknownValueError:
                print("Could not understand voice command")
    except sr.RequestError:
        print("Error requesting speech recognition")
    except Exception as e:
        print(f"Error: {e}")