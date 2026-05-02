"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import speech_recognition as sr
import pyttsx3
import json
import requests

# Initialize the Speech Recognition and Text-to-Speech libraries
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a dictionary to store device credentials and functionality
devices = {
    'lights': {
        'api_key': 'YOUR_LIGHTS_API_KEY',
        'url': 'YOUR_LIGHTS_API_ENDPOINT',
        'commands': ['turn on', 'turn off']
    },
    'thermostat': {
        'api_key': 'YOUR_THERMOSTAT_API_KEY',
        'url': 'YOUR_THERMOSTAT_API_ENDPOINT',
        'commands': ['set temperature to', 'increase/decrease temperature by']
    },
    'security system': {
        'api_key': 'YOUR_SECURITY_API_KEY',
        'url': 'YOUR_SECURITY_API_ENDPOINT',
        'commands': ['arm', 'disarm']
    }
}

# Define a function to process voice commands
def process_command(command):
    try:
        # Listen for audio from the microphone
        with sr.Microphone() as source:
            print('Listening...')
            audio = r.listen(source)

        # Recognize spoken text
        text = r.recognize_google(audio)

        print('You said:', text)

        # Extract the device and action from the spoken text
        for device, info in devices.items():
            for command_str in info['commands']:
                if command_str in text:
                    device = device
                    action = text.replace(command_str, '')

        # Send a request to the device API to execute the action
        if device and action:
            if device == 'lights':
                response = requests.post(info['url'], headers={'Authorization': info['api_key']}, json={'action': action})
            elif device == 'thermostat':
                response = requests.post(info['url'], headers={'Authorization': info['api_key']}, json={'action': action})
            elif device == 'security system':
                response = requests.post(info['url'], headers={'Authorization': info['api_key']}, json={'action': action})

            # Check if the request was successful
            if response.status_code == 200:
                print(f'Successfully executed action on {device}: {action}')
            else:
                print(f'Failed to execute action on {device}: {action}')

    except sr.RequestError as e:
        print(f'Speech recognition error: {e}')
    except sr.UnknownValueError:
        print('Could not understand your voice command')
    except requests.exceptions.RequestException as e:
        print(f'API request error: {e}')

# Define a function to listen for voice commands
def listen():
    while True:
        process_command('listen')

# Start the voice command listener
listen()