"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_001.txt
Run      : 3
"""

# Required libraries for handling API requests and data parsing
import requests
import json
import tweepy
from PIL import Image
import io
from PIL import ImageTk
import tkinter as tk

# Replace with your own Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Twitter API setup using Tweepy library
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function to fetch tweets and render them in a GUI
def fetch_and_render_tweets():
    try:
        # Fetch the last 10 tweets from the user's timeline
        tweets = api.user_timeline(screen_name="your_username", count=10)
        
        # Create a new Tkinter window
        window = tk.Tk()
        window.title("Social Media Feed")
        
        # Create a label to display the tweets
        label = tk.Label(window, wraplength=400, font=("Arial", 12))
        label.pack(padx=10, pady=10)
        
        # Loop through each tweet and render it in the GUI
        for tweet in tweets:
            # Get the tweet text and format it with newline characters
            text = tweet.text.replace("\n", "\n    ")
            
            # Create a new label for this tweet and add it to the window
            tweet_label = tk.Label(window, text=text, wraplength=400, font=("Arial", 12), fg="blue")
            tweet_label.pack(padx=10, pady=5)
            
            # If the tweet contains an image or video, download and render it
            if "media" in tweet.entities:
                # Get the media URL and download the image
                media_url = tweet.entities["media"][0]["media_url"]
                response = requests.get(media_url)
                image_data = response.content
                
                # Load the image using PIL and display it in the GUI
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((200, 200))  # Resize the image
                image_tk = ImageTk.PhotoImage(image)
                image_label = tk.Label(window, image=image_tk)
                image_label.image = image_tk  # Keep a reference to prevent the image from being garbage collected
                image_label.pack(padx=10, pady=5)
        
        # Start the Tkinter event loop
        window.mainloop()
    except tweepy.TweepError as e:
        # Handle any Twitter API errors
        print(f"Error fetching tweets: {e}")

# Call the function to fetch and render tweets
fetch_and_render_tweets()