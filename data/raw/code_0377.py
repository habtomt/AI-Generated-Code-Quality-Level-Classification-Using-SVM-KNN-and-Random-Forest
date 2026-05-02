"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy
import pandas as pd

# Load spacy model for NLP processing
nlp = spacy.load("en_core_web_sm")

# Load NLTK data
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Define a function to remove stop words and lemmatize words
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stop words and lemmatize
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalpha() and word.lower() not in stop_words]
    
    # Join the tokens back into a string
    return ' '.join(tokens)

# Define a function to detect spam
def detect_spam(text):
    # Use a simple regular expression to detect common spam keywords
    spam_keywords = ['buy now', 'click here', 'free trial', 'make money']
    for keyword in spam_keywords:
        if keyword in text.lower():
            return True
    return False

# Define a function to detect offensive language
def detect_offensive_language(text):
    # Use the spacy model to detect parts of speech
    doc = nlp(text)
    
    # Check for instances of swear words or hate speech
    for token in doc:
        if token.pos_ == 'ADJ' and token.text in ['bad', 'ugly', 'hateful', 'racist', 'sexist']:
            return True
    
    # Check for instances of profanity
    profane_words = ['ass', 'bitch', 'fuck', 'shit', 'damn']
    for word in profane_words:
        if word in text.lower():
            return True
    
    return False

# Define a function to detect sentiment
def detect_sentiment(text):
    # Use the NLTK VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    
    # Determine the sentiment based on the compound score
    if sentiment['compound'] >= 0.05:
        return 'positive'
    elif sentiment['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# Define a function to detect and remove inappropriate posts
def remove_inappropriate_posts(posts):
    removed_posts = []
    for post in posts:
        text = post['text']
        
        # Check for spam
        if detect_spam(text):
            print(f"Spam detected: {text}")
            removed_posts.append(post)
            continue
        
        # Check for offensive language
        if detect_offensive_language(text):
            print(f"Offensive language detected: {text}")
            removed_posts.append(post)
            continue
        
        # Check for sentiment
        sentiment = detect_sentiment(text)
        if sentiment == 'negative':
            print(f"Negative sentiment detected: {text}")
            removed_posts.append(post)
            continue
        
        # If the post passes all checks, add it to the list
        print(f"Post is acceptable: {text}")
    
    return removed_posts

# Example usage
posts = [
    {'text': 'I love this product!'},
    {'text': 'You are a bad person!'},
    {'text': 'Click here to buy now!'},
    {'text': 'This is a great product, but the customer service is terrible.'}
]

inappropriate_posts = remove_inappropriate_posts(posts)
for post in inappropriate_posts:
    print(post['text'])