"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_003.txt
Run      : 3
"""

# Required libraries
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import schedule
import time
from datetime import datetime

# Initialize NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize speech recognition object
r = sr.Recognizer()

# Function to handle voice commands
def handle_command(command):
    print(f"User said: {command}")

    # Tokenize the command
    tokens = word_tokenize(command)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Determine the task
    if 'set reminder' in tokens:
        # Extract the reminder details
        reminder_time = tokens[tokens.index('set') + 1]
        reminder_message = ' '.join(tokens[tokens.index('reminder') + 1:])

        # Schedule the reminder
        schedule.every().day.at(reminder_time).do(schedule_reminder, reminder_message)

        print(f"Reminder set for {reminder_time} - {reminder_message}")

    elif 'search' in tokens:
        # Extract the search query
        search_query = ' '.join(tokens[tokens.index('search') + 1:])

        # Search for information (for simplicity, just print a message)
        print(f"Searching for: {search_query}")

    elif 'schedule' in tokens:
        # Extract the schedule details
        schedule_time = tokens[tokens.index('schedule') + 1]
        schedule_message = ' '.join(tokens[tokens.index('at') + 1:])

        # Schedule the task
        schedule.every().day.at(schedule_time).do(schedule_task, schedule_message)

        print(f"Task scheduled for {schedule_time} - {schedule_message}")

    else:
        print("Invalid command")

# Function to handle reminders
def schedule_reminder(reminder_message):
    print(f"Reminder: {reminder_message}")

# Function to handle tasks
def schedule_task(schedule_message):
    print(f"Task: {schedule_message}")

# Main function
def main():
    while True:
        try:
            # Listen for voice commands
            with sr.Microphone() as source:
                print("Listening for voice commands...")
                audio = r.listen(source)

            # Recognize the voice command
            command = r.recognize_google(audio, language='en-US')
            handle_command(command)

            # Run scheduled tasks
            schedule.run_pending()
            time.sleep(1)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand your audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Run the main function
if __name__ == "__main__":
    main()