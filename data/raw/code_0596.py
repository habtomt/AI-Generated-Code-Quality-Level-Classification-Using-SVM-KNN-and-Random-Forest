"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import requests
import random
import string
import time
import os

# Replace with your Twilio account SID and auth token
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"
VERIFYING_PHONE_NUMBER = "USER_PHONE_NUMBER_TO_VERIFY"

def send_sms_code():
    # Generate a random verification code
    verification_code = ''.join(random.choices(string.digits, k=6))
    
    # Send the verification code to the user via SMS
    try:
        response = requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
            data={
                "To": VERIFYING_PHONE_NUMBER,
                "From": TWILIO_PHONE_NUMBER,
                "Body": f"Your verification code is: {verification_code}"
            },
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        )
        
        if response.status_code == 201:
            print("Verification code sent successfully.")
            return verification_code
        else:
            print("Failed to send verification code.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def verify_sms_code(entered_code):
    verification_code = send_sms_code()
    
    if verification_code:
        # Allow the user to enter the verification code
        entered_code = input("Enter the verification code: ")
        
        if entered_code == verification_code:
            print("Verification successful. Access granted.")
            return True
        else:
            print("Invalid verification code. Try again.")
            return False
    else:
        return False

def main():
    print("Welcome to the verification system.")
    
    VERIFYING_PHONE_NUMBER = input("Enter the phone number to verify: ")
    
    while True:
        entered_code = input("Enter the verification code: ")
        
        if verify_sms_code(entered_code):
            break
        else:
            print("Try again.")

if __name__ == "__main__":
    main()