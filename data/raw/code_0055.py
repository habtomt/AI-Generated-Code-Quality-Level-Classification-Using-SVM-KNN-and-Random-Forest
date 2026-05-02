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

ATTENDEES_FILE = "attendees.csv"
EVENT_DATE = datetime(2026, 5, 1, 18, 0, 0)

REMINDER_DAYS_BEFORE = 3


def load_attendees():
    try:
        return pd.read_csv(ATTENDEES_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "name", "email", "rsvp", "reminder_sent"
        ])


def save_attendees(df):
    df.to_csv(ATTENDEES_FILE, index=False)


def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    server.quit()


def send_invite(name, email):
    body = f"""
Hi {name},

You are invited to our exclusive event!

Event Date: {EVENT_DATE.strftime('%Y-%m-%d %H:%M')}

Please RSVP by replying or confirming via our system.

Looking forward to seeing you!
"""
    send_email(email, "You're Invited!", body)


def send_reminder(name, email):
    body = f"""
Hi {name},

This is a friendly reminder about the upcoming event on {EVENT_DATE.strftime('%Y-%m-%d %H:%M')}.

We hope to see you there!

Please make sure to RSVP if you haven't already.
"""
    send_email(email, "Event Reminder", body)


def send_invites():
    df = load_attendees()

    for _, row in df.iterrows():
        if row.get("rsvp") != "sent":
            send_invite(row["name"], row["email"])
            df.loc[df["email"] == row["email"], "rsvp"] = "sent"

    save_attendees(df)


def process_reminders():
    df = load_attendees()
    now = datetime.now()

    for idx, row in df.iterrows():
        if row.get("reminder_sent") == "yes":
            continue

        days_left = (EVENT_DATE - now).days

        if days_left <= REMINDER_DAYS_BEFORE:
            send_reminder(row["name"], row["email"])
            df.loc[idx, "reminder_sent"] = "yes"

    save_attendees(df)


def rsvp(email, status):
    df = load_attendees()
    if email in df["email"].values:
        df.loc[df["email"] == email, "rsvp"] = status
        save_attendees(df)


def main():
    send_invites()

    while True:
        process_reminders()
        time.sleep(3600)


if __name__ == "__main__":
    main()