"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_000.txt
Run      : 2
"""

import os
import time
from twilio.rest import Client

# Twilio account credentials
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
your_twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
my_twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

# Twilio client
client = Client(account_sid, auth_token)

# Function to send notification when new message is received
def send_notification(message):
    try:
        # Send SMS notification
        message = client.messages.create(
            from_=your_twilio_phone_number,
            body=f"New message from {message.from_}: {message.body[:50]}",  # Display snippet of message
            to=my_twilio_phone_number
        )
        print(f"Notification sent to {my_twilio_phone_number} with SID: {message.sid}")
    except Exception as e:
        print(f"Error sending notification: {e}")

# Function to monitor messages and trigger notifications
def monitor_messages():
    while True:
        # Get new messages
        messages = client.messages.list(from_=your_twilio_phone_number)
        
        # Process each new message
        for message in messages:
            send_notification(message)
        
        # Wait 1 minute before checking again
        time.sleep(60)

# Start monitoring messages
monitor_messages()