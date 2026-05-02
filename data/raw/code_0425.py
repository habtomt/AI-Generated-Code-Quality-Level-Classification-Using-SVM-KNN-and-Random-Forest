"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_003.txt
Run      : 3
"""

# Import necessary libraries
import tweepy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# Set up Twitter API credentials
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

# Set up Tweepy API object
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Set up NLTK sentiment analysis tool
nltk.download('vader_lexicon')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer()

# Define function to extract tweets and analyze sentiment
def analyze_sentiment(query, count):
    # Initialize sentiment dictionary
    sentiment = defaultdict(lambda: {"positive": 0, "negative": 0, "neutral": 0})

    # Search for tweets
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(count)

    # Analyze sentiment for each tweet
    for tweet in tweets:
        text = tweet.text
        # Remove stop words and punctuation
        text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
        # Analyze sentiment using NLTK VADER
        scores = sia.polarity_scores(text)
        if scores['compound'] > 0.05:
            sentiment['positive'] += 1
        elif scores['compound'] < -0.05:
            sentiment['negative'] += 1
        else:
            sentiment['neutral'] += 1

    return sentiment

# Define function to plot sentiment trends
def plot_sentiment Trends(sentiment_list):
    # Initialize lists to store sentiment data
    positive_list = []
    negative_list = []
    neutral_list = []

    # Extract sentiment data from list
    for sentiment in sentiment_list:
        positive_list.append(sentiment["positive"])
        negative_list.append(sentiment["negative"])
        neutral_list.append(sentiment["neutral"])

    # Create plot
    plt.figure(figsize=(10,6))
    plt.plot(positive_list, label="Positive")
    plt.plot(negative_list, label="Negative")
    plt.plot(neutral_list, label="Neutral")
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.title("Sentiment Trends")
    plt.legend()
    plt.show()

# Define main function to analyze sentiment and plot trends
def main():
    # Set query and count
    query = "#BrandName"  # Replace with brand name
    count = 100  # Number of tweets to analyze

    # Initialize list to store sentiment data
    sentiment_list = []

    # Analyze sentiment for each day
    for i in range(7):  # Analyze sentiment for 7 days
        date = (datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        try:
            # Extract tweets for day
            tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", since=date).items(count)
            # Analyze sentiment for day
            sentiment = analyze_sentiment(query, count)
            # Append sentiment data to list
            sentiment_list.append(sentiment)
        except Exception as e:
            print(f"Error on {date}: {str(e)}")

    # Plot sentiment trends
    plot_sentimentTrends(sentiment_list)

if __name__ == "__main__":
    main()