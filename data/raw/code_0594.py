"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_003.txt
Run      : 2
"""

# Import necessary libraries
import requests
import json
from twilio.rest import Client

# Set your account Sid and Auth Token from twilio.com/console
account_sid = "YOUR_ACCOUNT_SID"
auth_token = "YOUR_AUTH_TOKEN"
client = Client(account_sid, auth_token)

# Set your Twilio phone number and the customer's phone number
twilio_number = "+1234567890"
customer_number = "+9876543210"

# Function to send SMS notification
def send_sms_notification(message):
    try:
        # Use the Client to send an SMS message from Twilio
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=customer_number
        )
        
        # Print the SID of the sent message (optional)
        print("SID: ", message.sid)
    except requests.exceptions.RequestException as e:
        print("Error sending SMS:", e)
        return False

    return True

# Function to notify customers about updates or resolutions to their support inquiries
def notify_customer_update(inquiry_id, update_message):
    # Construct the SMS message
    message = f"Update on your support inquiry {inquiry_id}: {update_message}"
    
    # Send the SMS notification
    if send_sms_notification(message):
        print("Notification sent successfully")
    else:
        print("Failed to send notification")

# Example usage
if __name__ == "__main__":
    inquiry_id = "SUPPORT-123"
    update_message = "The issue has been resolved, thank you for your patience"
    notify_customer_update(inquiry_id, update_message)