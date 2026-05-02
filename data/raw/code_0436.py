"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import NMF
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from surprise import KNNWithMeans, Dataset, accuracy
from surprise.model_selection import train_test_split as split_surprise

# Load sample user behavior data
# Replace this with your actual dataset
data = {
    'user_id': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'item_id': [101, 102, 103, 101, 103, 102, 103, 102, 101, 103],
    'rating': [5, 4, 3, 5, 3, 4, 3, 5, 5, 3]
}
df = pd.DataFrame(data)

# Preprocess data for surprise library
ratings = []
for i in range(len(df)):
    ratings.append((df['user_id'][i], df['item_id'][i], df['rating'][i]))
ratings = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], rating_scale=(1, 5))

# Split data into training and testing sets
trainset, testset = split_surprise(ratings, test_size=.25)

# Define a simple collaborative filtering model using surprise
algo = KNNWithMeans(k=50, sim_options={'name': 'cosine', 'user_based': False})

# Train the model
algo.fit(trainset)

# Make predictions on the test set
predictions = algo.test(testset)

# Evaluate the model
accuracy.rmse(predictions)
accuracy.mae(predictions)

# Collaborative filtering using nearest neighbors
# Define the nearest neighbors model
nn_model = NearestNeighbors(n_neighbors=50, algorithm='brute', metric='cosine')

# Fit the model to the user ratings
nn_model.fit(df[['user_id', 'item_id']].values)

# Define a function to get recommendations for a user
def get_recommendations(user_id, num_recommendations):
    # Get the nearest neighbors for the user
    neighbors = nn_model.kneighbors(df.loc[df['user_id'] == user_id, 'user_id'].values.reshape(-1, 1), return_distance=False)[0]
    
    # Get the items rated by the nearest neighbors
    rated_items = df.loc[df['user_id'].isin(neighbors), 'item_id'].values
    
    # Get the items not rated by the user
    not_rated_items = np.setdiff1d(df['item_id'].unique(), rated_items)
    
    # Get the top num_recommendations items not rated by the user
    recommendations = not_rated_items[np.argsort(-df.loc[df['item_id'].isin(not_rated_items), 'rating'].mean())[:num_recommendations]]
    
    return recommendations

# Define a user
user_id = 1

# Get recommendations for the user
num_recommendations = 5
recommendations = get_recommendations(user_id, num_recommendations)
print(recommendations)

# Machine learning approach
# Define a feature set for the items
item_features = df.groupby('item_id')['rating'].mean().reset_index()

# Define a feature set for the users
user_features = df.groupby('user_id')['rating'].mean().reset_index()

# Define a random forest classification model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Define a pipeline to preprocess the data
preprocessor = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Define a feature transformer to one-hot encode categorical variables
feature_transformer = ColumnTransformer(
    transformers=[
        ('onehot', OneHotEncoder(), ['user_id', 'item_id'])
    ]
)

# Combine the preprocessors and feature transformers into a single pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('feature_transformer', feature_transformer),
    ('rf_model', rf_model)
])

# Fit the pipeline to the data
pipeline.fit(df[['user_id', 'item_id', 'rating']])

# Define a function to get recommendations for a user using the random forest model
def get_recommendations_rf(user_id, num_recommendations):
    # Preprocess the data
    preprocessed_data = pipeline['preprocessor'].transform(df[['user_id', 'item_id', 'rating']])
    
    # Get the top num_recommendations items for the user
    item_features['user_id'] = user_id
    item_features['preprocessed_rating'] = pipeline['preprocessor'].transform(item_features[['rating']])
    recommendations = item_features.nsmallest(num_recommendations, 'preprocessed_rating')['item_id']
    
    return recommendations

# Get recommendations for the user using the random forest model
recommendations = get_recommendations_rf(user_id, num_recommendations)
print(recommendations)