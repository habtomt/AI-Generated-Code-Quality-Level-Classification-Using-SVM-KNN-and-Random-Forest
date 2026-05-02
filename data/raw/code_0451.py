"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import calendar
import os

# Set up email credentials (replace with your own)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FROM_EMAIL = 'your-email@gmail.com'
PASSWORD = 'your-password'

# Set up event details (replace with your own)
EVENT_NAME = 'Event Invitation System'
EVENT_DATE = datetime(2024, 5, 1, 10, 0, 0)
EVENT_LOCATION = 'Event Location'

# Set up attendee list
attendees = [
    {'name': 'John Doe', 'email': 'john@example.com'},
    {'name': 'Jane Doe', 'email': 'jane@example.com'},
    # Add more attendees here...
]

# Function to send email invitation
def send_invitation(email, name):
    try:
        # Set up email content
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = f'You\'re Invited: {EVENT_NAME} on {EVENT_DATE.strftime("%B %d, %Y at %I:%M %p")} at {EVENT_LOCATION}'

        # Set up email body
        body = f'Dear {name},\n\nYou are cordially invited to {EVENT_NAME} on {EVENT_DATE.strftime("%B %d, %Y at %I:%M %p")} at {EVENT_LOCATION}.\n\nPlease RSVP by replying to this email.\n\nBest regards,\n[Your Name]'
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, email, text)
        server.quit()

        print(f'Email sent to {name} ({email})')
    except Exception as e:
        print(f'Error sending email to {name} ({email}): {e}')

# Function to track RSVPs
def track_rsvps():
    rsvps = {}
    for attendee in attendees:
        name = attendee['name']
        email = attendee['email']
        rsvp = input(f'{name} ({email}) - Are you attending? (yes/no): ')
        rsvps[name] = rsvp.lower() == 'yes'
        print(f'{name} ({email}) - RSVP: {rsvp.lower() == "yes"}')
    return rsvps

# Function to send reminders
def send_reminders(rsvps):
    today = datetime.today()
    one_day_before = EVENT_DATE - timedelta(days=1)
    two_days_before = one_day_before - timedelta(days=1)

    if today >= two_days_before:
        for attendee, attending in rsvps.items():
            if not attending:
                print(f'Sending reminder to {attendee}...')
                send_invitation(attendees[0]['email'], attendee)

# Main program
if __name__ == '__main__':
    # Send email invitations
    for attendee in attendees:
        send_invitation(attendee['email'], attendee['name'])

    # Track RSVPs
    rsvps = track_rsvps()

    # Send reminders
    send_reminders(rsvps)