# promotional_emails.py
import smtplib
import pytz
from datetime import datetime
from email.message import EmailMessage

def send_promotional_emails(subscribers):
    for sub in subscribers:
        user_tz = pytz.timezone(sub['timezone'])
        local_time = datetime.now(user_tz)

        if 9 <= local_time.hour <= 18:
            msg = EmailMessage()
            msg.set_content(f"Hi {sub['name']},\nCheck out our new deals!")
            msg['Subject'] = "Exclusive Offer for You"
            msg['From'] = "marketing@company.com"
            msg['To'] = sub['email']
            print(f"Sent to {sub['name']} at {local_time}")

subscribers = [
    {'name': 'Alice', 'email': 'alice@example.com', 'timezone': 'US/Eastern'},
    {'name': 'Bob', 'email': 'bob@example.com', 'timezone': 'Europe/London'}
]

if __name__ == "__main__":
    send_promotional_emails(subscribers)