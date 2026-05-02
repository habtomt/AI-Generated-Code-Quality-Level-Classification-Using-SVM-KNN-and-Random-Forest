"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_002.txt
Run      : 3
"""

# Import the required libraries
import requests
import json

# Define a class for SMS sender
class SMSender:
    def __init__(self, api_key, api_secret, sender_id):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sender_id = sender_id

    # Define a method to send SMS
    def send_sms(self, recipient, message):
        try:
            # Construct the API request
            url = "https://api.textlocal.in/send/"
            headers = {"Content-Type": "application/json"}
            data = {
                "api_key": self.api_key,
                "sender": self.sender_id,
                "numbers": recipient,
                "message": message,
                "route": "v2"
            }

            # Send the request and get the response
            response = requests.post(url, headers=headers, data=json.dumps(data))

            # Check if the response was successful
            if response.status_code == 201:
                print(f"SMS sent to {recipient}")
            else:
                print(f"Failed to send SMS to {recipient}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending SMS: {e}")

# Main function
def main():
    # Define the API credentials and sender ID
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    sender_id = "YOUR_SENDER_ID"

    # Define the SMS sender
    sms_sender = SMSender(api_key, api_secret, sender_id)

    # Define the list of subscribers
    subscribers = ["+919999999999", "+919999999998"]

    # Define the message to be sent
    message = "Get 10% off on your next purchase!"

    # Send SMS to each subscriber
    for recipient in subscribers:
        sms_sender.send_sms(recipient, message)

# Run the main function
if __name__ == "__main__":
    main()