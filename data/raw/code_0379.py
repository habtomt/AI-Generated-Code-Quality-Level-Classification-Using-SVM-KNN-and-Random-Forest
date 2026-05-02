"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_002.txt
Run      : 3
"""

# Required libraries for text analysis and machine learning
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# Import necessary libraries for data manipulation and visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Placeholders for API keys or credentials
YOUR_API_KEY = "YOUR_API_KEY"

# Function to preprocess text data
def preprocess_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords and lemmatize the tokens
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    # Join the tokens back into a string
    text = ' '.join(tokens)
    
    return text

# Load the dataset
# Assuming you have a CSV file named 'reviews.csv'
data = pd.read_csv('reviews.csv')

# Preprocess the text data
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

data['review'] = data['review'].apply(preprocess_text)

# Split the data into features (text) and target (label)
X = data['review']
y = data['label']

# Encode the target variable
le = LabelEncoder()
y = le.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the pipeline
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

# Define the hyperparameter tuning space
param_grid = {
    'vectorizer__max_features': [5000, 10000, 20000],
    'vectorizer__stop_words': ['english', None],
    'classifier__alpha': [0.1, 0.5, 1.0]
}

# Perform grid search with cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best parameters and the corresponding score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

# Print the best parameters and the score
print("Best Parameters:", best_params)
print("Best Score:", best_score)

# Train the model with the best parameters
best_pipeline = grid_search.best_estimator_
best_pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = best_pipeline.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, cmap='Blues')
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Confusion Matrix")
plt.show()