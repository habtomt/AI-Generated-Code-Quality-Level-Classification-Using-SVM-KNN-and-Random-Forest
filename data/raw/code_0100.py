#!/usr/bin/env python3

import time
from datetime import datetime, timedelta

# Mock SMS sender
def send_sms(phone, message):
    print(f"[SMS to {phone}] {message}")

# Sample appointment database
appointments = [
    {
        "name": "Alice",
        "phone": "+905551111111",
        "time": datetime.now() + timedelta(minutes=30)
    },
    {
        "name": "Bob",
        "phone": "+905552222222",
        "time": datetime.now() + timedelta(hours=2)
    },
    {
        "name": "Charlie",
        "phone": "+905553333333",
        "time": datetime.now() + timedelta(minutes=10)
    }
]

REMINDER_WINDOW = timedelta(minutes=60)

def check_and_send_reminders():
    now = datetime.now()

    for appt in appointments:
        if 0 <= (appt["time"] - now).total_seconds() <= REMINDER_WINDOW.total_seconds():
            message = f"Dear {appt['name']}, you have an appointment at {appt['time'].strftime('%H:%M')}."
            send_sms(appt["phone"], message)

def run_scheduler():
    print("SMS Reminder System Started...")
    while True:
        check_and_send_reminders()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()