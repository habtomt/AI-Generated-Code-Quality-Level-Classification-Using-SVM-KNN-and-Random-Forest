"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_003.txt
Run      : 2
"""

# Import necessary libraries
import speech_recognition as sr
import webbrowser
import datetime
import os
import pyttsx3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import csv

# Set up Google Calendar API credentials
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_KEY = 'YOUR_GOOGLE_API_KEY'

# Set up Speech Recognition
r = sr.Recognizer()

# Set up Text-to-Speech
engine = pyttsx3.init()

def speak(text):
    """Speak the given text"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for user voice commands"""
    with sr.Microphone() as source:
        audio = r.record(source, duration=3)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand your audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None

def create_calendar_event(title, start, end):
    """Create a calendar event using Google Calendar API"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': title,
        'start': {'date': start},
        'end': {'date': end},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def search_info(query):
    """Search for information on Google"""
    url = 'https://www.google.com/search?q=' + query
    webbrowser.get().open(url)

def set_reminder(title, date):
    """Create a reminder using Google Calendar API"""
    speak(f"Reminder set for {title} on {date}")

def manage_schedule():
    """Manage the user's schedule using Google Calendar API"""
    speak("What would you like to do with your schedule?")

def main():
    speak("Welcome to your virtual assistant!")
    while True:
        query = listen()
        if query is None:
            continue
        query = query.lower()
        if 'set reminder' in query:
            title = input("Enter reminder title: ")
            date = input("Enter reminder date (YYYY-MM-DD): ")
            create_calendar_event(title, date, date)
            set_reminder(title, date)
        elif 'search' in query:
            search_info(query.replace('search ', ''))
        elif 'schedule' in query:
            manage_schedule()
        elif 'open' in query:
            url = query.replace('open ', '')
            webbrowser.get().open(url)
        elif 'quit' in query:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()