"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.exceptions import ConvergenceWarning
import warnings
warnings.filterwarnings("ignore", category=ConvergenceWarning)
import pickle
import joblib

# Define a function to load and preprocess data
def load_and_preprocess_data(file_path):
    try:
        # Load data from CSV file
        data = pd.read_csv(file_path)
        
        # Preprocess text data
        data['text'] = data['text'].apply(lambda x: x.lower())
        
        # Split data into features (text) and target (label)
        X = data['text']
        y = data['label']
        
        return X, y
    
    except Exception as e:
        print("Error loading or preprocessing data: ", str(e))
        return None, None

# Define a function to train a machine learning model
def train_model(X_train, y_train, model_type):
    try:
        # Initialize the model
        if model_type == 'naive_bayes':
            model = MultinomialNB()
        elif model_type == 'random_forest':
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'logistic_regression':
            model = LogisticRegression(max_iter=1000)
        
        # Create a pipeline with TF-IDF vectorizer and the model
        pipe = Pipeline([('vectorizer', TfidfVectorizer()), ('model', model)])
        
        # Define hyperparameter tuning space
        param_grid = {
            'vectorizer__max_features': [5000, 10000, 20000],
            'model__n_estimators': [50, 100, 200]
        }
        
        # Perform grid search with cross-validation
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid_search = GridSearchCV(pipe, param_grid, cv=skf.split(X_train, y_train), n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        # Return the best model
        return grid_search.best_estimator_
    
    except Exception as e:
        print("Error training model: ", str(e))
        return None

# Define a function to save the model to a file
def save_model(model, file_path):
    try:
        # Save the model to a file
        joblib.dump(model, file_path)
        
        print("Model saved to file: ", file_path)
    
    except Exception as e:
        print("Error saving model to file: ", str(e))

# Define a function to load and preprocess data
def load_model(file_path):
    try:
        # Load the model from a file
        model = joblib.load(file_path)
        
        return model
    
    except Exception as e:
        print("Error loading model from file: ", str(e))
        return None

# Load data
X, y = load_and_preprocess_data('data.csv')

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a machine learning model
model = train_model(X_train, y_train, 'random_forest')

# Save the model to a file
save_model(model, 'model.joblib')

# Load the saved model
loaded_model = load_model('model.joblib')

# Evaluate the loaded model on the testing set
y_pred = loaded_model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))