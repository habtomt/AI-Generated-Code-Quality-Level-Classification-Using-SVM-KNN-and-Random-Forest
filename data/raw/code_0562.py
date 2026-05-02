"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_001.txt
Run      : 2
"""

import requests
import json
import os

# Set up your Discord Webhook URL and your app's version
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
APP_VERSION = "1.2.3"
IMPROVEMENTS = "Improved performance and fixed several bugs"
CHANGES = "Fixed login issue on iOS devices, Added new features"

def send_discord_notification():
    # Create a dictionary to hold the notification data
    notification_data = {
        "content": f"**New Version Available!**\n\nVersion: {APP_VERSION}\n\nImprovements: {IMPROVEMENTS}\n\nChanges:\n{CHANGES}"
    }
    
    try:
        # Send a POST request to the Discord Webhook URL with the notification data
        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(notification_data), headers={"Content-Type": "application/json"})
        
        # Check if the request was successful
        if response.status_code == 204:
            print("Notification sent successfully!")
        else:
            print(f"Error sending notification: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")

if __name__ == "__main__":
    # Call the function to send the notification
    send_discord_notification()