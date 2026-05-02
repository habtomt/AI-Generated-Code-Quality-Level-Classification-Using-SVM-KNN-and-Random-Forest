"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_004.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer

# Import necessary library for natural language processing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Import necessary library for collaborative filtering
import Surprise
from Surprise import KNNBasic
from Surprise import Dataset

# Import necessary library for data storage
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create table for user data if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        item_id TEXT,
        rating REAL,
        timestamp TEXT
    )
''')

# Function to get user ratings
def get_user_ratings(user_id):
    cursor.execute('SELECT rating FROM user_data WHERE user_id = ?', (user_id,))
    ratings = cursor.fetchall()
    return ratings

# Function to get item ratings
def get_item_ratings(item_id):
    cursor.execute('SELECT rating FROM user_data WHERE item_id = ?', (item_id,))
    ratings = cursor.fetchall()
    return ratings

# Function to get user-item interaction matrix
def get_user_item_matrix():
    cursor.execute('SELECT user_id, item_id, rating FROM user_data')
    data = cursor.fetchall()
    user_item_matrix = {}
    for row in data:
        user_id, item_id, rating = row
        if user_id not in user_item_matrix:
            user_item_matrix[user_id] = {}
        user_item_matrix[user_id][item_id] = rating
    return user_item_matrix

# Function to implement collaborative filtering
def collaborative_filtering(user_id, num_recommendations):
    user_item_matrix = get_user_item_matrix()
    user_ratings = get_user_ratings(user_id)
    user_item_matrix[user_id] = {}
    for rating in user_ratings:
        user_item_matrix[user_id][rating[1]] = rating[0]
    
    # Create Surprise dataset
    dataset = Dataset()
    for user, items in user_item_matrix.items():
        for item, rating in items.items():
            dataset.append(user, item, rating)
    
    # Create KNNBasic model
    knn = KNNBasic(k=50, sim_options={'name': 'cosine'})
    
    # Fit model to data
    knn.fit(dataset)
    
    # Get user's item ratings
    item_ratings = get_item_ratings(user_id)
    item_ids = [item[0] for item in item_ratings]
    
    # Get predicted ratings for items the user has not rated
    predictions = knn.test(user_id, item_ids)
    
    # Get top-N recommended items
    recommended_items = [item for item, rating in predictions.items() if rating > 0]
    recommended_items = recommended_items[:num_recommendations]
    
    return recommended_items

# Function to implement content-based filtering
def content_based_filtering(user_id):
    # Get user's item ratings
    item_ratings = get_item_ratings(user_id)
    item_ids = [item[0] for item in item_ratings]
    
    # Get item features
    cursor.execute('SELECT feature FROM item_features')
    features = cursor.fetchall()
    item_features = {}
    for feature in features:
        item_features[feature[0]] = feature[1]
    
    # Calculate similarity between items
    similarities = {}
    for item_id in item_ids:
        similarities[item_id] = {}
        for other_item_id, feature in item_features.items():
            if item_id != other_item_id:
                similarity = similarity_function(item_id, other_item_id, item_features)
                similarities[item_id][other_item_id] = similarity
    
    # Get recommended items
    recommended_items = {}
    for item_id in item_ids:
        recommended_items[item_id] = {}
        for other_item_id, similarity in similarities[item_id].items():
            if similarity > 0:
                recommended_items[item_id][other_item_id] = similarity
    
    return recommended_items

# Function to calculate similarity between items
def similarity_function(item_id1, item_id2, item_features):
    feature1 = item_features[item_id1]
    feature2 = item_features[item_id2]
    similarity = 0
    for i in range(len(feature1)):
        similarity += feature1[i] * feature2[i]
    return similarity

# Function to implement hybrid filtering
def hybrid_filtering(user_id):
    # Implement collaborative filtering
    collaborative_recommendations = collaborative_filtering(user_id, 10)
    
    # Implement content-based filtering
    content_based_recommendations = content_based_filtering(user_id)
    
    # Combine recommendations
    hybrid_recommendations = {}
    for item_id in collaborative_recommendations:
        if item_id in content_based_recommendations:
            hybrid_recommendations[item_id] = content_based_recommendations[item_id]
    
    return hybrid_recommendations

# Function to get product recommendations for a user
def get_product_recommendations(user_id):
    # Implement hybrid filtering
    hybrid_recommendations = hybrid_filtering(user_id)
    
    # Get top-N recommended products
    recommended_products = {}
    for item_id, similarity in hybrid_recommendations.items():
        recommended_products[item_id] = similarity
    
    # Get product features
    cursor.execute('SELECT feature FROM product_features')
    features = cursor.fetchall()
    product_features = {}
    for feature in features:
        product_features[feature[0]] = feature[1]
    
    # Get recommended products with features
    recommended_products_with_features = {}
    for item_id, similarity in recommended_products.items():
        recommended_products_with_features[item_id] = {'similarity': similarity, 'features': product_features[item_id]}
    
    return recommended_products_with_features

# Test the system
user_id = '12345'
recommended_products = get_product_recommendations(user_id)
print(recommended_products)