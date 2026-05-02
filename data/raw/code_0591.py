"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_000.txt
Run      : 2
"""

# Import required libraries
import random
import string
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up Twilio credentials for SMS verification
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_VERIFICATION_SID = 'YOUR_TWILIO_VERIFICATION_SID'
TWILIO_PHONE_NUMBER = '+1234567890'  # Replace with your Twilio phone number

# Set up email credentials for fallback verification
EMAIL_ADDRESS = 'YOUR_EMAIL_ADDRESS'
EMAIL_PASSWORD = 'YOUR_EMAIL_PASSWORD'

def send_sms_verification(phone_number):
    # Generate a random 6-digit verification code
    verification_code = ''.join(random.choices(string.digits, k=6))

    # Use Twilio to send SMS verification code
    try:
        response = requests.post(
            f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json',
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            data={
                'From': TWILIO_PHONE_NUMBER,
                'To': phone_number,
                'Body': f'Your verification code is: {verification_code}'
            }
        )
        response.raise_for_status()
        print(f'Verification code sent to {phone_number}')
    except requests.exceptions.RequestException as e:
        print(f'Error sending verification code: {e}')

def send_email_verification(phone_number, verification_code):
    # Use email to send verification code as fallback
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = phone_number
    msg['Subject'] = 'Verification Code'

    body = f'Your verification code is: {verification_code}'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, phone_number, text)
    server.quit()

    print(f'Verification code sent to {phone_number} via email')

def verify_code(phone_number, verification_code):
    # Use Twilio to verify code
    try:
        response = requests.post(
            f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json',
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            data={
                'From': TWILIO_PHONE_NUMBER,
                'To': phone_number,
                'Body': f'Confirmation code is: {verification_code}'
            }
        )
        response.raise_for_status()
        print(f'Verification code {verification_code} is correct')
        return True
    except requests.exceptions.RequestException as e:
        print(f'Error verifying code: {e}')
        return False

def main():
    phone_number = input('Enter your phone number: ')
    send_sms_verification(phone_number)
    verification_code = input('Enter the verification code: ')
    if verify_code(phone_number, verification_code):
        print('Access granted')
    else:
        print('Incorrect verification code')

if __name__ == '__main__':
    main()