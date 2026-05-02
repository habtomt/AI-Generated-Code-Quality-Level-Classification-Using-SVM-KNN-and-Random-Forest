"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_000.txt
Run      : 1
"""

# Import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

# Download required NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Function to preprocess text data
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Join the tokens back into a string
    text = ' '.join(tokens)
    
    return text

# Load the dataset
try:
    data = pd.read_csv('dataset.csv')
except FileNotFoundError:
    print("The dataset file was not found. Please ensure it is in the correct location.")
    exit()

# Preprocess the text data
data['text'] = data['text'].apply(preprocess_text)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer(max_features=10000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a machine learning model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Evaluate the model
predictions = model.predict(X_test_tfidf)
print(classification_report(y_test, predictions))

# Function to predict new posts
def is_inappropriate_post(post):
    # Preprocess the post
    post = preprocess_text(post)
    
    # Vectorize the post
    post_tfidf = vectorizer.transform([post])
    
    # Make a prediction
    prediction = model.predict(post_tfidf)
    
    return prediction[0] == 1

# Example usage
new_post = "This is a sample inappropriate comment!"
if is_inappropriate_post(new_post):
    print("Inappropriate post detected!")
else:
    print("Post is appropriate.")