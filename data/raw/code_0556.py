"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_000.txt
Run      : 1
"""

# Import the required libraries
import tkinter as tk
from tkinter import messagebox
import threading
import time

# Define the function to display notification
def show_notification(sender, message):
    # Limit the message snippet to 50 characters
    message_snippet = message[:50] + "..." if len(message) > 50 else message

    # Display the notification
    tkinter_messagebox = messagebox.showinfo(f"New Message from {sender}", message_snippet)

# Define the function to request permission for notifications
def request_permission():
    # Request permission for notifications
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter window
    tkinter_messagebox = messagebox.showinfo("Notification Permission", "This application needs permission to show notifications.")
    root.destroy()

    # Wait for the user to respond
    response = tkinter_messagebox
    if response == "OK":
        return True
    else:
        return False

# Define the function to receive new message
def receive_new_message(sender, message):
    # Request permission for notifications
    permission_granted = request_permission()
    if permission_granted:
        # Display the notification
        show_notification(sender, message)

# Simulating receiving a message
def simulate_receiving_message():
    while True:
        sender = "Alice"
        message = "Hello! How are you doing today?"
        receive_new_message(sender, message)
        time.sleep(5)  # Wait for 5 seconds before receiving the next message

# Start the simulation
thread = threading.Thread(target=simulate_receiving_message)
thread.daemon = True  # Allow the thread to exit when the main program exits
thread.start()

# Keep the main program running
while True:
    pass