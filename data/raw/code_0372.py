"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Define a function to preprocess text data
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize text into words
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Stem words using Porter Stemmer
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    # Join tokens back into a string
    text = ' '.join(tokens)
    
    return text

# Define a function to train a Naive Bayes classifier
def train_classifier(X_train, y_train):
    # Initialize a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit the vectorizer to the training data and transform both the training and testing data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    # Train a Naive Bayes classifier
    clf = MultinomialNB()
    clf.fit(X_train_tfidf, y_train)
    
    return clf, vectorizer

# Define a function to evaluate the classifier
def evaluate_classifier(clf, vectorizer, X_test, y_test, X_new):
    # Transform the testing data and new text data
    X_test_tfidf = vectorizer.transform(X_test)
    X_new_tfidf = vectorizer.transform(X_new)
    
    # Make predictions on the testing data and new text data
    y_pred = clf.predict(X_test_tfidf)
    y_pred_new = clf.predict(X_new_tfidf)
    
    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    
    return accuracy, report, matrix, y_pred_new

# Load the dataset (replace with your actual dataset)
df = pd.read_csv('forum_data.csv')

# Preprocess the text data
df['text'] = df['text'].apply(preprocess_text)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Train a Naive Bayes classifier
clf, vectorizer = train_classifier(X_train, y_train)

# Evaluate the classifier
accuracy, report, matrix, y_pred_new = evaluate_classifier(clf, vectorizer, X_test, y_test, X_test)

# Print the evaluation metrics
print(f'Accuracy: {accuracy:.3f}')
print('Classification Report:')
print(report)
print('Confusion Matrix:')
print(matrix)

# Define a function to classify new text data
def classify_text(text):
    # Preprocess the text
    text = preprocess_text(text)
    
    # Transform the text into a TF-IDF vector
    text_tfidf = vectorizer.transform([text])
    
    # Make a prediction
    prediction = clf.predict(text_tfidf)
    
    # Return the prediction
    return prediction[0]

# Test the classification function
new_text = 'This is a new text that we want to classify.'
prediction = classify_text(new_text)
print(f'Prediction: {prediction}')

# Define a function to remove inappropriate posts
def remove_inappropriate_posts(texts):
    # Classify each text
    classifications = [classify_text(text) for text in texts]
    
    # Remove texts with a negative label
    texts = [text for text, classification in zip(texts, classifications) if classification == 1]
    
    # Return the list of texts
    return texts

# Test the function to remove inappropriate posts
texts = ['This is a text that we want to remove.', 'This is another text that we want to keep.']
inappropriate_texts = remove_inappropriate_posts(texts)
print(f'Inappropriate texts:')
print(inappropriate_texts)