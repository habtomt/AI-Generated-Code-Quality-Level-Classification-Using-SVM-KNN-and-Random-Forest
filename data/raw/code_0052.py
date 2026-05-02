import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import time

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_password"

SUBSCRIBERS_FILE = "subscribers.csv"

EMAIL_SEQUENCE = [
    {
        "subject": "Welcome to Our Community!",
        "body": "Thanks for joining us! We're excited to have you on board."
    },
    {
        "subject": "Getting Started Guide",
        "body": "Here’s how you can get the most out of our products and services."
    },
    {
        "subject": "Tips & Tricks",
        "body": "Discover advanced tips to maximize your experience with us."
    },
    {
        "subject": "Exclusive Offer Inside",
        "body": "As a valued new subscriber, here’s a special offer just for you!"
    }
]

def load_subscribers():
    return pd.read_csv(SUBSCRIBERS_FILE)

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Sent: {subject} -> {to_email}")
    except Exception as e:
        print(f"Error sending to {to_email}: {e}")

def run_email_sequence(subscribers):
    for _, user in subscribers.iterrows():
        email = user["email"]

        for i, email_step in enumerate(EMAIL_SEQUENCE):
            send_email(email, email_step["subject"], email_step["body"])
            time.sleep(2)

def main():
    subscribers = load_subscribers()
    run_email_sequence(subscribers)

if __name__ == "__main__":
    main()