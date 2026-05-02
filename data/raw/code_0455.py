"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_003.txt
Run      : 3
"""

# Import necessary libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os

# Load configuration from JSON file
config_file = 'config.json'
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Configuration file {config_file} not found.")
    exit(1)

# Load credentials from configuration
SMTP_SERVER = config['smtp_server']
SMTP_PORT = config['smtp_port']
FROM_EMAIL = config['from_email']
FROM_PASSWORD = config['from_password']

# Define function to send email
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, FROM_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Define function to handle new subscriptions
def handle_new_subscription(email):
    body = f"""
    Welcome to our newsletter!

    Thank you for subscribing. You will now receive regular updates from us.

    To manage your email preferences, please reply to this email with one of the following commands:
    - UNSUBSCRIBE to unsubscribe from our newsletter
    - PREFERENCES to change your email preferences
    """
    send_email(email, "Confirmation: Newsletter Subscription", body)

# Define function to manage email preferences
def manage_preferences(email, preferences):
    body = f"""
    Email preferences updated for {email}

    Preferences: {preferences}
    """
    send_email(email, "Email Preferences Updated", body)

# Define function to unsubscribe from newsletter
def unsubscribe(email):
    body = f"""
    You have been unsubscribed from our newsletter.

    If you want to resubscribe, please reply to this email with a message.
    """
    send_email(email, "Unsubscribe: Newsletter", body)

# Main program
if __name__ == "__main__":
    # Create configuration file if it does not exist
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump({
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'from_email': 'your-email@gmail.com',
                'from_password': 'your-password'
            }, f)

    # Handle new subscription
    new_email = input("Enter new email: ")
    handle_new_subscription(new_email)

    # Manage email preferences
    email = input("Enter email to manage preferences: ")
    preferences = input("Enter new preferences (e.g. daily, weekly): ")
    manage_preferences(email, preferences)

    # Unsubscribe from newsletter
    email = input("Enter email to unsubscribe: ")
    unsubscribe(email)