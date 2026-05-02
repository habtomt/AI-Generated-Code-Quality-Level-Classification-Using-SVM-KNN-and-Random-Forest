"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_003.txt
Run      : 1
"""

import speech_recognition as sr
import pyttsx3
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import json
import webbrowser

# If you modify these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()
    except Exception as e:
        print("Error: " + str(e))
        speak("Sorry, I could not understand. Please try again.")
        return None

def authenticate_google():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def search_for(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
    except Exception as e:
        print("Error: " + str(e))
        speak("Sorry, I could not find any results.")

def set_reminder(text):
    try:
        speak(f"Reminder set for {text}")
        with open("reminders.txt", "a") as f:
            f.write(f"Reminder: {text}\n")
    except Exception as e:
        print("Error: " + str(e))
        speak("Sorry, I could not save the reminder.")

def manage_schedule(creds):
    try:
        from googleapiclient.discovery import build
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary',
                                              timeMin=now,
                                              maxResults=10,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        speak("Here are your upcoming events.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            speak(event['summary'])
    except Exception as e:
        print("Error: " + str(e))
        speak("Sorry, I could not find any events.")

def main():
    creds = authenticate_google()
    speak("Hello, how can I assist you today?")
    
    while True:
        command = listen_command()
        if command:
            if "set a reminder" in command:
                speak("What should I remind you about?")
                reminder_text = listen_command()
                if reminder_text:
                    set_reminder(reminder_text)

            elif "search for" in command:
                query = command.replace("search for", "").strip()
                speak(f"Searching for {query}")
                search_for(query)

            elif "manage schedule" in command:
                manage_schedule(creds)

            elif "exit" in command:
                speak("Goodbye!")
                break

            elif "help" in command:
                speak("You can say:")
                speak("  - Set a reminder")
                speak("  - Search for something")
                speak("  - Manage schedule")
                speak("  - Exit")
                speak("  - Help")

if __name__ == "__main__":
    main()