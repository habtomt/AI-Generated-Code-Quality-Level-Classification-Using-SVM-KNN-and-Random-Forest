"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_000.txt
Run      : 2
"""

# Import the required libraries
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import pyperclip

# Download the required NLTK data if not already downloaded
nltk.download('vader_lexicon')

# Initialize the sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.
    
    Args:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary containing the sentiment scores.
    """
    try:
        # Analyze the sentiment of the text
        scores = sia.polarity_scores(text)
        
        # Determine the sentiment based on the compound score
        if scores['compound'] >= 0.05:
            sentiment = 'Positive'
        elif scores['compound'] <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        # Return the sentiment scores and sentiment
        return {'sentiment': sentiment, **scores}
    except Exception as e:
        # Handle any exceptions that occur during analysis
        print(f"Error analyzing sentiment: {str(e)}")
        return {'error': str(e)}

def get_text_from_clipboard():
    """
    Get the text from the clipboard.
    
    Returns:
    str: The text from the clipboard.
    """
    try:
        # Get the text from the clipboard
        text = pyperclip.paste()
        
        # Return the text
        return text
    except Exception as e:
        # Handle any exceptions that occur while getting the clipboard text
        print(f"Error getting clipboard text: {str(e)}")
        return ''

def main():
    # Get the text from the clipboard
    text = get_text_from_clipboard()
    
    # Analyze the sentiment of the text
    sentiment = analyze_sentiment(text)
    
    # Print the sentiment scores and sentiment
    print("Sentiment Analysis:")
    print(f"Sentiment: {sentiment['sentiment']}")
    print(f"Scores: {sentiment}")

if __name__ == "__main__":
    main()