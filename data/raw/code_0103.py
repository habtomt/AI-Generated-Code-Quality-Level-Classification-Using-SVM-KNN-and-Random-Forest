#!/usr/bin/env python3

import time
from datetime import datetime

# Mock SMS sender
def send_sms(phone, message):
    print(f"[SMS to {phone}] {message}")

# Order database
orders = [
    {
        "order_id": "A1001",
        "customer": "Alice",
        "phone": "+905551111111",
        "status": "Order Placed"
    },
    {
        "order_id": "B2002",
        "customer": "Bob",
        "phone": "+905552222222",
        "status": "Order Placed"
    }
]

def notify_status_update(order, old_status, new_status):
    message = (
        f"Order {order['order_id']} Update: {old_status} -> {new_status}. "
        f"Current status: {new_status}."
    )
    send_sms(order["phone"], message)

def update_order_status(order_id, new_status):
    for order in orders:
        if order["order_id"] == order_id:
            old_status = order["status"]
            order["status"] = new_status
            notify_status_update(order, old_status, new_status)
            return

def track_order_flow():
    print("Real-time Order Tracking SMS System Started...\n")

    time.sleep(2)
    update_order_status("A1001", "Packed")

    time.sleep(2)
    update_order_status("B2002", "Packed")

    time.sleep(2)
    update_order_status("A1001", "Shipped")

    time.sleep(2)
    update_order_status("B2002", "Shipped")

    time.sleep(2)
    update_order_status("A1001", "Out for Delivery")

    time.sleep(2)
    update_order_status("A1001", "Delivered")

    time.sleep(2)
    update_order_status("B2002", "Delivered")

def run_system():
    track_order_flow()

if __name__ == "__main__":
    run_system()