"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_003.txt
Run      : 2
"""

# Import necessary libraries
import tweepy
import pandas as pd
import numpy as np
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Set up Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Set up authentication for Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define a function to collect tweets based on a keyword
def collect_tweets(keyword):
    # Create a Tweepy API object
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang='en').items(100)
    return tweets

# Define a function to analyze the sentiment of a tweet
def analyze_sentiment(tweet):
    # Use TextBlob to analyze the sentiment of the tweet
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Define a function to create a word cloud from a list of tweets
def create_wordcloud(tweets):
    # Join all the tweets into a single string
    text = ' '.join([tweet.text for tweet in tweets])
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400).generate(text)
    # Display the word cloud
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Define a function to plot a bar chart of sentiment trends over time
def plot_sentiment_trends(tweets):
    # Create a list to store the sentiment values
    sentiment_values = []
    # Create a list to store the dates
    dates = []
    # Loop through the tweets
    for tweet in tweets:
        # Get the date of the tweet
        date = tweet.created_at.date()
        # Get the sentiment of the tweet
        sentiment = analyze_sentiment(tweet.text)
        # Append the sentiment value and date to the lists
        sentiment_values.append(sentiment)
        dates.append(date)
    # Create a bar chart
    plt.bar(dates, [sentiment_values.count('Positive'), sentiment_values.count('Neutral'), sentiment_values.count('Negative')])
    plt.xlabel('Date')
    plt.ylabel('Sentiment')
    plt.title('Sentiment Trends Over Time')
    plt.show()

# Define the main function
def main():
    # Collect tweets based on a keyword
    keyword = '#Apple'
    tweets = collect_tweets(keyword)
    # Create a DataFrame from the tweets
    df = pd.DataFrame([(tweet.id, tweet.text, tweet.created_at.date()) for tweet in tweets], columns=['id', 'text', 'date'])
    # Analyze the sentiment of each tweet
    df['sentiment'] = df['text'].apply(analyze_sentiment)
    # Create a word cloud from the tweets
    create_wordcloud(tweets)
    # Plot a bar chart of sentiment trends over time
    plot_sentiment_trends(tweets)

# Run the main function
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'An error occurred: {e}')