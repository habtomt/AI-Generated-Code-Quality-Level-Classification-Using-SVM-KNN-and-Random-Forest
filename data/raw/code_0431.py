"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_004.txt
Run      : 1
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.sparse.linalg import svds
import numpy as np

# Load your dataset
def load_data(file_path):
    try:
        ratings_data = pd.read_csv(file_path)
        return ratings_data
    except Exception as e:
        print(f"Error loading data: {e}")

# Prepare your data
def prepare_data(ratings_data):
    try:
        # Split the data into a training set and a test set
        train_data, test_data = train_test_split(ratings_data, test_size=0.2, random_state=42)
        return train_data, test_data
    except Exception as e:
        print(f"Error preparing data: {e}")

# Build the recommendation system using collaborative filtering
def build_recommendation_system(train_data):
    try:
        # Create a user-item matrix
        user_product_matrix = train_data.pivot(index='user_id', columns='product_id', values='rating').fillna(0)
        matrix = user_product_matrix.to_numpy()

        # Normalize the matrix
        user_ratings_mean = np.mean(matrix, axis=1)
        matrix_demeaned = matrix - user_ratings_mean.reshape(-1, 1)

        # Perform Singular Value Decomposition
        U, sigma, Vt = svds(matrix_demeaned, k=50)

        # Convert sigma to a diagonal matrix
        sigma = np.diag(sigma)

        # Make predictions
        predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        predicted_ratings_df = pd.DataFrame(predicted_ratings, columns=user_product_matrix.columns)
        return predicted_ratings_df
    except Exception as e:
        print(f"Error building recommendation system: {e}")

# Make recommendations
def recommend_products(predicted_ratings_df, user_id, num_recommendations=5):
    try:
        user_index = user_id - 1  # Assuming user_id starts from 1
        sorted_user_predictions = predicted_ratings_df.iloc[user_index].sort_values(ascending=False)
        
        # Products the user has already rated
        user_data = train_data[train_data.user_id == user_id]
        user_rated_products = user_data.product_id.values
        
        # Recommendations
        recommendations = sorted_user_predictions[~sorted_user_predictions.index.isin(user_rated_products)].head(num_recommendations)
        
        print("Recommendations for User ID:", user_id)
        print(recommendations)
    except Exception as e:
        print(f"Error making recommendations: {e}")

# Main function
def main():
    file_path = 'user_product_ratings.csv'  # replace with your file path
    ratings_data = load_data(file_path)
    train_data, test_data = prepare_data(ratings_data)
    predicted_ratings_df = build_recommendation_system(train_data)
    recommend_products(predicted_ratings_df, user_id=1, num_recommendations=5)

if __name__ == "__main__":
    main()