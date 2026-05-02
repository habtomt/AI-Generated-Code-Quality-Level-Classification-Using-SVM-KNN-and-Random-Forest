"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
import requests
import json
import os

# Set your API credentials
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

# Set the API endpoint URL
API_URL = "https://api.twitter.com/2/tweets"

# Set the headers and parameters for the API request
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

params = {
    "tweet.fields": "id,author_id,text,created_at,entities.media",
    "max_results": 10
}

# Try to fetch data from the API
try:
    # Send a GET request to the API endpoint
    response = requests.get(API_URL, headers=headers, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        # Parse the response as JSON
        data = json.loads(response.text)
        
        # Print the fetched data
        print(json.dumps(data, indent=4))
        
        # Function to render posts
        def render_posts(data):
            # Check if the data contains media
            if "includes" in data and "media" in data["includes"]:
                # Loop through each tweet
                for tweet in data["data"]:
                    # Print the tweet text and author
                    print(f"Tweet by @{tweet['author_id']}: {tweet['text']}")
                    
                    # Check if the tweet contains media
                    if tweet["entities"]["media"]:
                        # Loop through each media
                        for media in tweet["entities"]["media"]:
                            # Check if the media is an image or video
                            if media["type"] == "photo":
                                # Print the image URL
                                print(f"Image: {media['media_url_https']}")
                            elif media["type"] == "video":
                                # Print the video URL
                                print(f"Video: {media['url']}")
        
        # Call the function to render posts
        render_posts(data)
    
    # If the response was not successful, print an error message
    else:
        print(f"Error: {response.status_code}")
except requests.exceptions.RequestException as e:
    # Catch any request exceptions and print an error message
    print(f"Error: {e}")