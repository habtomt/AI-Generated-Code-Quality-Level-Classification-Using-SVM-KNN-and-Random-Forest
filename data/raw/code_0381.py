"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_004.txt
Run      : 3
"""

# Importing required libraries
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
import nltk
import re
import string
import pandas as pd
import numpy as np

# Downloading required NLTK resources
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

class CommentFilter:
    def __init__(self):
        # Initialize sentiment intensity analyzer
        self.sia = SentimentIntensityAnalyzer()
        
        # Load dataset for training
        try:
            self.df = pd.read_csv('comment_dataset.csv')
        except FileNotFoundError:
            print("Dataset not found.")
            exit()

        # Preprocess data
        self.preprocess_data()
        
        # Train Naive Bayes classifier
        self.train_model()

    def preprocess_data(self):
        # Remove punctuation and convert all text to lowercase
        self.df['comment'] = self.df['comment'].apply(lambda x: re.sub('['+string.punctuation+']', '', x).lower())
        
        # Tokenize comments
        self.df['comment'] = self.df['comment'].apply(word_tokenize)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        self.df['comment'] = self.df['comment'].apply(lambda x: [word for word in x if word not in stop_words])
        
        # Lemmatize words
        self.df['comment'] = self.df['comment'].apply(lambda x: [WordNetLemmatizer().lemmatize(word) for word in x])
        
        # Join tokens back into strings
        self.df['comment'] = self.df['comment'].apply(lambda x: ' '.join(x))

    def train_model(self):
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.df['comment'], self.df['label'], test_size=0.2, random_state=42)
        
        # Count vectorizer for feature extraction
        cv = CountVectorizer()
        X_train_count = cv.fit_transform(X_train)
        X_test_count = cv.transform(X_test)
        
        # Train Naive Bayes classifier
        from sklearn.naive_bayes import MultinomialNB
        clf = MultinomialNB()
        clf.fit(X_train_count, y_train)
        
        # Predict using trained model
        y_pred = clf.predict(X_test_count)
        
        # Evaluate model
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    def filter_comments(self, comments):
        # Predict using trained model
        from sklearn.feature_extraction.text import CountVectorizer
        cv = CountVectorizer()
        comment_count = cv.fit_transform(comments)
        predicted_labels = self.clf.predict(comment_count)
        
        # Return filtered comments
        return predicted_labels

if __name__ == "__main__":
    # Create comment filter instance
    cf = CommentFilter()
    
    # Filter a list of comments
    comments = [
        "This is a great article!",
        "I don't like this article at all.",
        "This is a terrible article.",
        "I'm so happy to read this article."
    ]
    
    filtered_labels = cf.filter_comments(comments)
    
    # Print filtered labels
    for i, label in enumerate(filtered_labels):
        print(f"Comment {i+1}: {comments[i]}. Label: {label}")