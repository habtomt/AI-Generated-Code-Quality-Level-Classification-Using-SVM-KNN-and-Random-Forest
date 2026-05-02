"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_002.txt
Run      : 2
"""

import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset (assuming it's a CSV file)
# For this example, we'll use a dummy dataset
data = {
    'review': [
        'Great product, highly recommend!',
        'This product is terrible!',
        'I love this product, it\'s amazing!',
        'The product is okay, but not great.',
        'This product is amazing!',
        'I would not recommend this product.',
        'This product is great!',
        'The product is terrible!',
        'I love this product!',
        'This product is okay.'
    ],
    'is_fake': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 0 for genuine, 1 for fake
}
df = pd.DataFrame(data)

# Preprocess the text data
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)

df['review'] = df['review'].apply(preprocess_text)

# Split the data into training and testing sets
X = df['review']
y = df['is_fake']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the training data and transform both the training and testing data
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Naive Bayes classifier on the training data
clf = MultinomialNB()
clf.fit(X_train_tfidf, y_train)

# Make predictions on the testing data
y_pred = clf.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.3f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))