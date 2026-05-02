"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
import requests
import json
import os

# Social media API credentials (Replace with your actual credentials)
TWITTER_API_KEY = "YOUR_TWITTER_API_KEY"
TWITTER_API_SECRET = "YOUR_TWITTER_API_SECRET"
FACEBOOK_APP_ID = "YOUR_FACEBOOK_APP_ID"
FACEBOOK_APP_SECRET = "YOUR_FACEBOOK_APP_SECRET"
INSTAGRAM_CLIENT_ID = "YOUR_INSTAGRAM_CLIENT_ID"
INSTAGRAM_CLIENT_SECRET = "YOUR_INSTAGRAM_CLIENT_SECRET"

# Define a class for social media sharing
class SocialMediaSharer:
    def __init__(self):
        self.twitter_api_key = TWITTER_API_KEY
        self.twitter_api_secret = TWITTER_API_SECRET
        self.facebook_app_id = FACEBOOK_APP_ID
        self.facebook_app_secret = FACEBOOK_APP_SECRET
        self.instagram_client_id = INSTAGRAM_CLIENT_ID
        self.instagram_client_secret = INSTAGRAM_CLIENT_SECRET

    def share_on_twitter(self, content):
        # Set up Twitter API request headers and parameters
        headers = {
            'Authorization': f'Bearer {self.get_twitter_bearer_token()}',
            'Content-Type': 'application/json'
        }
        params = {
            'status': content
        }

        try:
            # Make a POST request to the Twitter API to share the content
            response = requests.post('https://api.twitter.com/2/statuses/update.json', headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sharing on Twitter: {e}")

    def share_on_facebook(self, content):
        # Set up Facebook API request headers and parameters
        headers = {
            'Authorization': f'Bearer {self.get_facebook_access_token()}',
            'Content-Type': 'application/json'
        }
        params = {
            'message': content
        }

        try:
            # Make a POST request to the Facebook API to share the content
            response = requests.post('https://graph.facebook.com/v13.0/me/feed', headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sharing on Facebook: {e}")

    def share_on_instagram(self, content):
        # Set up Instagram API request headers and parameters
        headers = {
            'Authorization': f'Bearer {self.get_instagram_access_token()}',
            'Content-Type': 'application/json'
        }
        params = {
            'caption': content
        }

        try:
            # Make a POST request to the Instagram API to share the content
            response = requests.post('https://graph.instagram.com/v13.0/media', headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sharing on Instagram: {e}")

    def get_twitter_bearer_token(self):
        # Set up Twitter API request headers and parameters
        headers = {
            'Authorization': f'Bearer {self.get_twitter_access_token()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'grant_type': 'client_credentials'
        }

        try:
            # Make a POST request to the Twitter API to get a bearer token
            response = requests.post('https://api.twitter.com/oauth2/token', headers=headers, params=params)
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            print(f"Error getting Twitter bearer token: {e}")

    def get_facebook_access_token(self):
        # Set up Facebook API request headers and parameters
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.facebook_app_id,
            'client_secret': self.facebook_app_secret
        }

        try:
            # Make a POST request to the Facebook API to get an access token
            response = requests.post('https://graph.facebook.com/v13.0/oauth/access_token', headers=headers, params=params)
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            print(f"Error getting Facebook access token: {e}")

    def get_instagram_access_token(self):
        # Set up Instagram API request headers and parameters
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.instagram_client_id,
            'client_secret': self.instagram_client_secret
        }

        try:
            # Make a POST request to the Instagram API to get an access token
            response = requests.post('https://graph.instagram.com/v13.0/oauth/access_token', headers=headers, params=params)
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            print(f"Error getting Instagram access token: {e}")

# Usage
if __name__ == '__main__':
    sharer = SocialMediaSharer()
    content = "Hello, world!"

    sharer.share_on_twitter(content)
    sharer.share_on_facebook(content)
    sharer.share_on_instagram(content)