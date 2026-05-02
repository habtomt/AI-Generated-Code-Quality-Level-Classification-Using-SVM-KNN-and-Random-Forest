"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os

# Email credentials
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"

# SMTP server details
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# List of email subscribers
subscribers = [
    ("Subscriber 1", "subscriber1@example.com"),
    ("Subscriber 2", "subscriber2@example.com"),
    ("Subscriber 3", "subscriber3@example.com"),
]

# Email sequence structure (list of emails, each with a subject, body, and send date)
email_sequence = [
    {
        "subject": "Welcome to our newsletter!",
        "body": "Dear subscriber, welcome to our newsletter! We're excited to have you on board.",
        "send_date": datetime.date(2024, 4, 25),
    },
    {
        "subject": "Discover our top products!",
        "body": "Check out our latest products and services.",
        "send_date": datetime.date(2024, 5, 1),
    },
    {
        "subject": "Tips for getting the most out of our services",
        "body": "Here are some valuable tips to help you get the most out of our services.",
        "send_date": datetime.date(2024, 5, 8),
    },
    {
        "subject": "Exclusive offer for our subscribers!",
        "body": "Don't miss out on our exclusive offer. Use code SUBSCRIBER15 at checkout.",
        "send_date": datetime.date(2024, 5, 15),
    },
]

# Send emails to subscribers
def send_email(subscriber_email, email_data):
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = subscriber_email
    msg['Subject'] = email_data['subject']

    # Attach email body
    msg.attach(MIMEText(email_data['body'], 'plain'))

    # Create SMTP connection
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Send email
    try:
        server.sendmail(EMAIL_ADDRESS, subscriber_email, msg.as_string())
        print(f"Email sent to {subscriber_email}")
    except Exception as e:
        print(f"Error sending email to {subscriber_email}: {e}")
    finally:
        server.quit()

# Main loop
for subscriber in subscribers:
    for email_data in email_sequence:
        # Check if the send date has arrived
        if email_data['send_date'] == datetime.date.today():
            send_email(subscriber[1], email_data)

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Create a file to save the email sequence
    with open("email_sequence.txt", "w") as f:
        f.write(str(email_sequence))
    print("Email sequence saved to email_sequence.txt")