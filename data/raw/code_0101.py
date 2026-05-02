#!/usr/bin/env python3

import time
from datetime import datetime

# Mock SMS sender
def send_sms(phone, message):
    print(f"[SMS to {phone}] {message}")

# Subscriber database
subscribers = [
    {"name": "Alice", "phone": "+905551111111", "opt_in": True},
    {"name": "Bob", "phone": "+905552222222", "opt_in": True},
    {"name": "Charlie", "phone": "+905553333333", "opt_in": False},
]

# Promotional campaigns
campaigns = [
    {
        "title": "Weekend Discount",
        "message": "Enjoy 20% off all products this weekend only!",
        "active": True
    },
    {
        "title": "New Arrivals",
        "message": "Check out our new collection now in stores!",
        "active": True
    }
]

def get_active_campaigns():
    return [c for c in campaigns if c["active"]]

def send_campaigns():
    active_campaigns = get_active_campaigns()

    for campaign in active_campaigns:
        full_message = f"{campaign['title']}: {campaign['message']}"

        for sub in subscribers:
            if sub["opt_in"]:
                send_sms(sub["phone"], full_message)

def add_subscriber(name, phone):
    subscribers.append({
        "name": name,
        "phone": phone,
        "opt_in": True
    })

def unsubscribe(phone):
    for sub in subscribers:
        if sub["phone"] == phone:
            sub["opt_in"] = False

def run_marketing_system():
    print("Promotional SMS System Started...")

    while True:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending campaigns...")
        send_campaigns()
        time.sleep(300)  # every 5 minutes

if __name__ == "__main__":
    run_marketing_system()