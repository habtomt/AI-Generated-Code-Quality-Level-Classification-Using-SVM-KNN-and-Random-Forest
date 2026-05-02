"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_000.txt
Run      : 1
"""

# Import the TextBlob library
from textblob import TextBlob

def analyze_sentiment(text):
    try:
        # Create a TextBlob object
        blob = TextBlob(text)

        # Get the sentiment analysis result
        sentiment = blob.sentiment

        # Determine polarity and subjectivity
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        # Analyze the polarity to determine positive, neutral, or negative
        if polarity > 0:
            sentiment_label = "Positive"
        elif polarity < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        return sentiment_label, polarity, subjectivity

    except Exception as e:
        # Handle any exceptions that occur during sentiment analysis
        print(f"An error occurred: {e}")
        return None

# Example usage
text = "I love this product! It works wonderfully."
result = analyze_sentiment(text)

if result:
    sentiment_label, polarity, subjectivity = result
    print(f"Sentiment: {sentiment_label}")
    print(f"Polarity: {polarity}")
    print(f"Subjectivity: {subjectivity}")
else:
    print("Failed to analyze sentiment.")