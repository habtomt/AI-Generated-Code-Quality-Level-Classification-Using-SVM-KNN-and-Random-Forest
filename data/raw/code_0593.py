"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_002.txt
Run      : 2
"""

# Import required libraries
import requests
import json

# Set your Twilio account credentials
TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"

class SMSMessenger:
    def __init__(self, account_sid, auth_token, phone_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number

    def send_sms(self, recipient_number, message):
        # Set the URL for the Twilio API
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"

        # Set the authentication parameters
        auth = (self.account_sid, self.auth_token)

        # Set the message parameters
        params = {
            "From": self.phone_number,
            "To": recipient_number,
            "Body": message
        }

        try:
            # Send a POST request to the Twilio API
            response = requests.post(url, auth=auth, data=params)

            # Check if the request was successful
            if response.status_code == 201:
                print("SMS sent successfully!")
            else:
                print("Error sending SMS:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending SMS:", e)

# Create an instance of the SMSMessenger class
messenger = SMSMessenger(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)

# Define a list of subscribers
subscribers = [
    {"number": "+1234567890", "name": "John Doe"},
    {"number": "+9876543210", "name": "Jane Doe"}
]

# Define the promotional message
message = "Get 20% off your next purchase! Use code TWILIO20 at checkout."

# Send the promotional message to each subscriber
for subscriber in subscribers:
    print(f"Sending SMS to {subscriber['name']} ({subscriber['number']})...")
    messenger.send_sms(subscriber["number"], message)
    print()