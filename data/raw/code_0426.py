"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_004.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error
from math import sqrt
from collections import defaultdict
import numpy as np

# Function to load data
def load_data(file_path):
    try:
        # Load data from csv file
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")

# Function to preprocess data
def preprocess_data(data):
    try:
        # Drop unnecessary columns
        data.drop(["id", "date"], axis=1, inplace=True)
        
        # Convert categorical variables into numerical variables
        categorical_cols = data.select_dtypes(include=["object"]).columns
        data[categorical_cols] = data[categorical_cols].apply(lambda x: pd.Categorical(x).codes)
        
        # Scale data using MinMaxScaler
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)
        
        # Convert scaled data back into DataFrame
        data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
        
        return data_scaled
    except Exception as e:
        print(f"Error preprocessing data: {e}")

# Function to split data into training and testing sets
def split_data(data):
    try:
        # Split data into features and target
        X = data.drop("rating", axis=1)
        y = data["rating"]
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Error splitting data: {e}")

# Function to implement collaborative filtering using NearestNeighbors
def collaborative_filtering(X_train, X_test):
    try:
        # Create NearestNeighbors model
        nn_model = NearestNeighbors(n_neighbors=10)
        
        # Fit model to training data
        nn_model.fit(X_train)
        
        # Get nearest neighbors for each user in testing set
        distances, indices = nn_model.kneighbors(X_test)
        
        # Get predicted ratings for each user in testing set
        predicted_ratings = []
        for i in range(len(indices)):
            user_ratings = X_train.iloc[indices[i]]
            predicted_rating = np.mean(user_ratings)
            predicted_ratings.append(predicted_rating)
        
        return predicted_ratings
    except Exception as e:
        print(f"Error implementing collaborative filtering: {e}")

# Function to implement content-based filtering using PCA and Logistic Regression
def content_based_filtering(X_train, X_test):
    try:
        # Apply PCA to reduce dimensionality
        pca = PCA(n_components=5)
        X_train_pca = pca.fit_transform(X_train)
        X_test_pca = pca.transform(X_test)
        
        # Split data into features and target
        X_train_pca = pd.DataFrame(X_train_pca)
        X_test_pca = pd.DataFrame(X_test_pca)
        y_train = X_train["rating"]
        y_test = X_test["rating"]
        
        # Train Logistic Regression model
        lr_model = LogisticRegression()
        lr_model.fit(X_train_pca, y_train)
        
        # Make predictions on testing data
        predicted_ratings = lr_model.predict(X_test_pca)
        
        return predicted_ratings
    except Exception as e:
        print(f"Error implementing content-based filtering: {e}")

# Function to implement hybrid approach
def hybrid_approach(X_train, X_test):
    try:
        # Implement collaborative filtering
        predicted_ratings_colab = collaborative_filtering(X_train, X_test)
        
        # Implement content-based filtering
        predicted_ratings_content = content_based_filtering(X_train, X_test)
        
        # Combine predicted ratings from both approaches
        predicted_ratings = []
        for i in range(len(predicted_ratings_colab)):
            predicted_rating = (predicted_ratings_colab[i] + predicted_ratings_content[i]) / 2
            predicted_ratings.append(predicted_rating)
        
        return predicted_ratings
    except Exception as e:
        print(f"Error implementing hybrid approach: {e}")

# Function to evaluate model performance
def evaluate_model(y_test, predicted_ratings):
    try:
        # Calculate mean squared error
        mse = mean_squared_error(y_test, predicted_ratings)
        rmse = sqrt(mse)
        
        # Calculate mean absolute error
        mae = np.mean(np.abs(y_test - predicted_ratings))
        
        return rmse, mae
    except Exception as e:
        print(f"Error evaluating model: {e}")

# Load data
data = load_data("user_product_interactions.csv")

# Preprocess data
data_scaled = preprocess_data(data)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = split_data(data_scaled)

# Implement collaborative filtering
predicted_ratings_colab = collaborative_filtering(X_train, X_test)

# Implement content-based filtering
predicted_ratings_content = content_based_filtering(X_train, X_test)

# Implement hybrid approach
predicted_ratings_hybrid = hybrid_approach(X_train, X_test)

# Evaluate model performance
rmse_colab, mae_colab = evaluate_model(y_test, predicted_ratings_colab)
rmse_content, mae_content = evaluate_model(y_test, predicted_ratings_content)
rmse_hybrid, mae_hybrid = evaluate_model(y_test, predicted_ratings_hybrid)

# Print results
print("Collaborative Filtering:")
print(f"RMSE: {rmse_colab}, MAE: {mae_colab}")
print("Content-Based Filtering:")
print(f"RMSE: {rmse_content}, MAE: {mae_content}")
print("Hybrid Approach:")
print(f"RMSE: {rmse_hybrid}, MAE: {mae_hybrid}")