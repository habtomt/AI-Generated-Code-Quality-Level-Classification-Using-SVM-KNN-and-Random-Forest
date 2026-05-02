"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_003.txt
Run      : 3
"""

# Required libraries
import requests
from twilio.rest import Client

# Twilio Account Credentials
ACCOUNT_SID = "YOUR_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1234567890"
SMS_SERVICE_SID = "YOUR_SMS_SERVICE_SID"

def send_sms(message, to_number):
    """
    Sends an SMS notification to the provided number.
    
    :param message: The SMS message to send.
    :param to_number: The phone number to send the SMS to.
    """
    try:
        # Twilio Client Initialization
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        # Send SMS using Twilio
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body=message,
            to=to_number,
            messaging_service_sid=SMS_SERVICE_SID
        )
        
        print(f"SMS sent to {to_number}: {message.sid}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")

def notify_customer_update(inquiry_id, customer_name, message):
    """
    Notifies a customer about an update to their support inquiry.
    
    :param inquiry_id: The ID of the support inquiry.
    :param customer_name: The name of the customer.
    :param message: The update message to send.
    """
    # Retrieve customer phone number from database (replace with actual database query)
    customer_phone_number = "+9876543210"
    
    send_sms(f"Hi {customer_name}, an update on your support inquiry {inquiry_id}: {message}", customer_phone_number)

def notify_customer_resolution(inquiry_id, customer_name):
    """
    Notifies a customer that their support inquiry has been resolved.
    
    :param inquiry_id: The ID of the support inquiry.
    :param customer_name: The name of the customer.
    """
    # Retrieve customer phone number from database (replace with actual database query)
    customer_phone_number = "+9876543210"
    
    send_sms(f"Hi {customer_name}, your support inquiry {inquiry_id} has been resolved.", customer_phone_number)

# Example usage
notify_customer_update("INQ-001", "John Doe", "The issue is being looked into.")
notify_customer_resolution("INQ-001", "John Doe")