"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_000.txt
Run      : 3
"""

# Required imports
import requests
import json
import logging
import schedule
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Telegram API endpoint and credentials
TELEGRAM_API_ENDPOINT = 'https://api.telegram.org'
YOUR_API_KEY = 'YOUR_API_KEY'
YOUR_CHAT_ID = 'YOUR_CHAT_ID'

# Function to send notification to Telegram
def send_notification(message):
    try:
        url = f'{TELEGRAM_API_ENDPOINT}/bot{YOUR_API_KEY}/sendMessage'
        params = {'chat_id': YOUR_CHAT_ID, 'text': message}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logging.info('Notification sent successfully')
        else:
            logging.error(f'Error sending notification: {response.status_code}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error sending notification: {e}')

# Function to process new messages
def process_new_messages():
    try:
        url = f'{TELEGRAM_API_ENDPOINT}/bot{YOUR_API_KEY}/getUpdates'
        params = {'timeout': 1}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            updates = json.loads(response.text)['result']
            for update in updates:
                # Get the last message in the update
                last_message = update['message']
                # Get the sender's name and a snippet of the message
                sender = last_message['from']['username']
                message = last_message['text'][:50] + '...'
                # Send a notification to Telegram
                send_notification(f'New message from {sender}: {message}')
        else:
            logging.error(f'Error getting updates: {response.status_code}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error getting updates: {e}')

# Schedule the process_new_messages function to run every minute
schedule.every(1).minutes.do(process_new_messages)

# Run the scheduled task indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)