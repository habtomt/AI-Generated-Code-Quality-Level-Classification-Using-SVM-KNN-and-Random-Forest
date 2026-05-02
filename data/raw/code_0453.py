"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_001.txt
Run      : 3
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pandas as pd

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "your_email@gmail.com"
PASSWORD = "your_password"

# Placeholder API keys and credentials
API_KEY = "YOUR_API_KEY"

# List of subscribers
subscribers = pd.DataFrame({
    "Name": ["John Doe", "Jane Doe"],
    "Email": ["john@example.com", "jane@example.com"]
})

# Automated email sequence
email_sequence = [
    {
        "subject": "Welcome to our community!",
        "body": "Dear {name},\n\nWelcome to our community! We're excited to have you on board.\n\nBest regards, {team}",
        "send_after": datetime.now()  # Send immediately
    },
    {
        "subject": "Product A: Features and Benefits",
        "body": "Dear {name},\n\nWe'd like to introduce you to our product A. Here are some of its key features and benefits:\n\n{features}\n\nBest regards, {team}",
        "send_after": datetime.now() + timedelta(days=2)  # Send 2 days after subscription
    },
    {
        "subject": "Product B: Use Cases and Examples",
        "body": "Dear {name},\n\nWe'd like to show you some use cases and examples of our product B:\n\n{use_cases}\n\nBest regards, {team}",
        "send_after": datetime.now() + timedelta(days=5)  # Send 5 days after subscription
    },
    {
        "subject": "Exclusive Offer: Discount for New Subscribers",
        "body": "Dear {name},\n\nAs a new subscriber, we'd like to offer you an exclusive discount on our products:\n\n{discount}\n\nBest regards, {team}",
        "send_after": datetime.now() + timedelta(days=7)  # Send 7 days after subscription
    }
]

def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email: ", str(e))

def automate_email_sequence(subscribers):
    for index, row in subscribers.iterrows():
        for email in email_sequence:
            if email["send_after"] <= datetime.now():
                send_email(row["Email"], email["subject"].format(name=row["Name"], team="Your Team", features="Product features", use_cases="Product use cases", discount="Discount code"), email["body"].format(name=row["Name"], team="Your Team", features="Product features", use_cases="Product use cases", discount="Discount code"))
            else:
                print("Email not sent yet, scheduled for ", email["send_after"])

automate_email_sequence(subscribers)