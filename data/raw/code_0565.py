"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
import requests
import json
import os

# Set your notification service API credentials
DISCORD_BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
DISCORD_CHANNEL_ID = 'YOUR_DISCORD_CHANNEL_ID'

# Set the promotional offer details
PROMOTIONAL_OFFER = {
    'title': 'Limited Time Offer',
    'description': 'Get 20% off on all products for the next 24 hours!',
    'expires_at': '2024-03-16 23:59:59'
}

def send_discord_notification(title, description, expires_at):
    # Set up the Discord Webhook URL
    url = f'https://discord.com/api/webhooks/{DISCORD_BOT_TOKEN}/{DISCORD_CHANNEL_ID}'

    # Create the notification payload
    payload = {
        'embeds': [
            {
                'title': title,
                'description': description,
                'footer': {
                    'text': f'Expires at {expires_at}',
                    'icon_url': 'https://example.com/icon.png'
                },
                'color': 3447003  # Orange color
            }
        ]
    }

    # Convert the payload to JSON
    json_payload = json.dumps(payload)

    try:
        # Send the notification using the Discord Webhook API
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json_payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print('Notification sent successfully!')
    except requests.exceptions.RequestException as e:
        print(f'Error sending notification: {e}')

def main():
    # Send the promotional offer notification
    send_discord_notification(PROMOTIONAL_OFFER['title'], PROMOTIONAL_OFFER['description'], PROMOTIONAL_OFFER['expires_at'])

if __name__ == '__main__':
    main()