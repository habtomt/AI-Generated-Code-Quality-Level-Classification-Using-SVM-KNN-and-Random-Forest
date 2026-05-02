"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_002.txt
Run      : 2
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from PIL import Image
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from twython import Twython
from instagram_private_api import Client

# Set up social media API credentials
YOUR_TWITTER_CONSUMER_KEY = 'YOUR_TWITTER_CONSUMER_KEY'
YOUR_TWITTER_CONSUMER_SECRET = 'YOUR_TWITTER_CONSUMER_SECRET'
YOUR_TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
YOUR_TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

YOUR_INSTAGRAM_USERNAME = 'YOUR_INSTAGRAM_USERNAME'
YOUR_INSTAGRAM_PASSWORD = 'YOUR_INSTAGRAM_PASSWORD'

YOUR_GOOGLE_CREDENTIALS_FILE = 'YOUR_GOOGLE_CREDENTIALS_FILE.json'

# Set up social media API clients
twitter = Twython(YOUR_TWITTER_CONSUMER_KEY,
                  YOUR_TWITTER_CONSUMER_SECRET,
                  YOUR_TWITTER_ACCESS_TOKEN,
                  YOUR_TWITTER_ACCESS_TOKEN_SECRET)

instagram_api = Client(YOUR_INSTAGRAM_USERNAME, YOUR_INSTAGRAM_PASSWORD)

# Set up Google API client
creds = Credentials.from_authorized_user_file(YOUR_GOOGLE_CREDENTIALS_FILE)
service = build('drive', 'v3', credentials=creds)

def share_to_twitter(text, image_path=None):
    """
    Share a message to Twitter.
    """
    try:
        if image_path:
            image = Image.open(image_path)
            image.thumbnail((1024, 1024))  # Resize image
            image.save('thumbnail.jpg', 'JPEG')
            media = twitter.upload_media(media='thumbnail.jpg')
            twitter.update_status(status=text, media_ids=[media['media_id']])
            os.remove('thumbnail.jpg')  # Remove temporary image
        else:
            twitter.update_status(status=text)
        print('Shared to Twitter successfully!')
    except Exception as e:
        print(f'Error sharing to Twitter: {e}')

def share_to_instagram(text, image_path=None):
    """
    Share a message to Instagram.
    """
    try:
        if image_path:
            image = Image.open(image_path)
            image.thumbnail((1080, 1080))  # Resize image
            image.save('thumbnail.jpg', 'JPEG')
            caption = text
            media = instagram_api.upload_photo('thumbnail.jpg', caption=caption)
            print(f'Shared to Instagram with caption: {caption}')
            os.remove('thumbnail.jpg')  # Remove temporary image
        else:
            print('No image provided for Instagram share.')
    except Exception as e:
        print(f'Error sharing to Instagram: {e}')

def share_to_drive(text, image_path=None):
    """
    Share a message to Google Drive.
    """
    try:
        if image_path:
            file_name = os.path.basename(image_path)
            file_metadata = {'name': file_name}
            media = MediaFileUpload(image_path, mimetype='image/jpeg')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'Uploaded image to Google Drive with ID: {file.get("id")}')
        print('Shared to Google Drive successfully!')
    except HttpError as e:
        print(f'Error sharing to Google Drive: {e}')

# Example usage:
share_to_twitter('Hello, world!', 'image.jpg')
share_to_instagram('Hello, world!', 'image.jpg')
share_to_drive('Hello, world!', 'image.jpg')