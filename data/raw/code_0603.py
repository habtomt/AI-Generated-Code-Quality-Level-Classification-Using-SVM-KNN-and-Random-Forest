"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_002.txt
Run      : 1
"""

# Import necessary libraries
import tweepy
import requests
import json
import os

# Set up API credentials
FACEBOOK_APP_ID = 'YOUR_FACEBOOK_APP_ID'
FACEBOOK_APP_SECRET = 'YOUR_FACEBOOK_APP_SECRET'
TWITTER_API_KEY = 'YOUR_TWITTER_API_KEY'
TWITTER_API_SECRET = 'YOUR_TWITTER_API_SECRET_KEY'
TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

# Set up Facebook
def get_facebook_access_token():
    # Get Facebook access token
    auth_url = f'https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id={FACEBOOK_APP_ID}&client_secret={FACEBOOK_APP_SECRET}'
    response = requests.get(auth_url)
    data = json.loads(response.text)
    access_token = data['access_token']
    return access_token

def share_on_facebook(content):
    # Share content on Facebook
    access_token = get_facebook_access_token()
    url = f'https://graph.facebook.com/v13.0/me/feed?access_token={access_token}'
    payload = {'message': content, 'link': 'https://yourwebsite.com/content-to-share'}
    response = requests.post(url, data=payload)
    return response.status_code

# Set up Twitter
def get_twitter_access_token():
    # Get Twitter access token
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    return auth

def share_on_twitter(content):
    # Share content on Twitter
    auth = get_twitter_access_token()
    api = tweepy.API(auth)
    try:
        api.update_status(status=content)
        return True
    except tweepy.TweepError as e:
        print(f'Error sharing on Twitter: {e}')
        return False

# Usage
if __name__ == '__main__':
    content = 'Check out this amazing content!'
    print('Sharing on Facebook:', share_on_facebook(content))
    print('Sharing on Twitter:', share_on_twitter(content))