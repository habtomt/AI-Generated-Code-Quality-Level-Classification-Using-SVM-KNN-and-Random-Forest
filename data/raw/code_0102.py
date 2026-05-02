#!/usr/bin/env python3

import time
from datetime import datetime

# Mock SMS sender
def send_sms(phone, message):
    print(f"[SMS to {phone}] {message}")

# Support ticket database
tickets = [
    {
        "id": 1,
        "customer": "Alice",
        "phone": "+905551111111",
        "status": "Open"
    },
    {
        "id": 2,
        "customer": "Bob",
        "phone": "+905552222222",
        "status": "In Progress"
    }
]

def notify_customer(ticket, update_message):
    message = f"Ticket #{ticket['id']} Update: {update_message} (Status: {ticket['status']})"
    send_sms(ticket["phone"], message)

def update_ticket_status(ticket_id, new_status):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = new_status
            notify_customer(ticket, f"Your support request has been updated to '{new_status}'")
            return

def simulate_support_flow():
    print("Customer Support SMS Notification System Started...\n")

    time.sleep(2)
    update_ticket_status(1, "In Progress")

    time.sleep(2)
    update_ticket_status(2, "Resolved")

    time.sleep(2)
    update_ticket_status(1, "Resolved")

def run_system():
    simulate_support_flow()

if __name__ == "__main__":
    run_system()