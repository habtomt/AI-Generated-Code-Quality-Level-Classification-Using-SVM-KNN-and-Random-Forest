"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_002.txt
Run      : 1
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os

# Configure SMTP server (example uses Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@gmail.com'
SMTP_PASSWORD = os.environ.get('GMAIL_PASSWORD')  # Secure password storage

# Sample user and event data
users = [
    {
        'name': 'Alice',
        'email': 'alice@example.com',
        'events': [
            {
                'title': 'Team Meeting',
                'datetime': datetime(2023, 10, 15, 15, 0),  # Year, Month, Day, Hour, Minute
                'details': 'Monthly team meeting to discuss project updates.'
            }
        ]
    },
    {
        'name': 'Bob',
        'email': 'bob@example.com',
        'events': [
            {
                'title': 'Product Launch',
                'datetime': datetime(2023, 10, 20, 10, 0),
                'details': 'Launch event for the new product line.'
            }
        ]
    },
]

def send_email(subject, body, recipient_email):
    """
    Send an email to the specified recipient.
    """
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, recipient_email, msg.as_string())
        server.quit()
        print(f'Email sent to {recipient_email}')
    except Exception as e:
        print(f'Failed to send email to {recipient_email}. Error: {e}')

def notify_users():
    """
    Notify users about their upcoming events.
    """
    current_time = datetime.now()
    notify_delta = timedelta(days=1)  # Notify 1 day before the event

    for user in users:
        for event in user['events']:
            time_until_event = event['datetime'] - current_time
            if time_until_event <= notify_delta:
                subject = f'Reminder: Upcoming Event - {event["title"]}'
                body = f"""Hello {user['name']},

This is a reminder for your upcoming event:

Title: {event['title']}
Date and Time: {event['datetime'].strftime('%Y-%m-%d %H:%M')}
Details: {event['details']}

Thank you,
Your Events Team
"""
                send_email(subject, body, user['email'])

if __name__ == '__main__':
    notify_users()