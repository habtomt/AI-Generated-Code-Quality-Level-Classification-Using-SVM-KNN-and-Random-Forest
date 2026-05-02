"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_000.txt
Run      : 3
"""

# Import the necessary libraries
from textblob import TextBlob
import tweepy

# Define Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Set up the Tweepy API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function to analyze sentiment of a single tweet
def analyze_sentiment(tweet):
    try:
        # Create a TextBlob object
        analysis = TextBlob(tweet)
        
        # Get the sentiment polarity
        polarity = analysis.sentiment.polarity
        
        # Determine the sentiment based on polarity
        if polarity > 0:
            return "Positive"
        elif polarity == 0:
            return "Neutral"
        else:
            return "Negative"
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Error"

# Function to get tweets from Twitter API
def get_tweets(query, count):
    try:
        # Search for tweets
        tweets = api.search(q=query, count=count)
        
        # Get the text of each tweet
        tweet_texts = [tweet.text for tweet in tweets]
        
        # Analyze the sentiment of each tweet
        sentiments = [analyze_sentiment(tweet) for tweet in tweet_texts]
        
        # Return a dictionary with the sentiments
        return {"sentiments": sentiments, "tweets": tweet_texts}
    except tweepy.TweepError as e:
        print(f"Error getting tweets: {e}")
        return None

# Example usage
query = "Python"
count = 10

result = get_tweets(query, count)

if result is not None:
    print("Sentiments:")
    for sentiment, tweet in zip(result["sentiments"], result["tweets"]):
        print(f"{tweet}: {sentiment}")
else:
    print("No tweets found.")