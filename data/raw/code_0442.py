"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_000.txt
Run      : 1
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz
import os
import time

# Sample subscriber data
subscribers = [
    {"name": "Alice", "email": "alice@example.com", "timezone": "America/New_York"},
    {"name": "Bob", "email": "bob@example.com", "timezone": "Europe/London"},
    # Add more subscribers as needed
]

# Function to send personalized emails
def send_email(subscriber):
    name = subscriber["name"]
    email = subscriber["email"]
    timezone = subscriber["timezone"]

    # Compute the subscriber's local time
    local_tz = pytz.timezone(timezone)
    local_time = datetime.now(local_tz)

    # Check if it's an appropriate time to send the email (e.g., between 8 AM and 8 PM)
    if 8 <= local_time.hour <= 20:
        # Create the email
        from_addr = os.environ.get('FROM_EMAIL')  # Use environment variable for security
        to_addr = email
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = "Special Offer Just for You!"
        
        # Customize the email content
        body = f"""
        Hi {name},

        We are excited to offer you an exclusive discount!

        Best Regards,
        Your Company
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            server = smtplib.SMTP(os.environ.get('SMTP_SERVER'), int(os.environ.get('SMTP_PORT')))  # Replace with your SMTP server details
            server.starttls()
            server.login(os.environ.get('FROM_EMAIL'), os.environ.get('EMAIL_PASSWORD'))  # Use environment variables for security
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {name} at {email}")
        except Exception as e:
            print(f"Failed to send email to {name}: {str(e)}")

# Iterate over the subscriber list and send emails with a delay to avoid being flagged as spam
for subscriber in subscribers:
    send_email(subscriber)
    time.sleep(60)  # Wait for 1 minute before sending the next email