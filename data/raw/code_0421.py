"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import pickle

# Load the dataset
# Assuming we have a CSV file named 'user_data.csv' with the following columns:
#   - user_id: unique identifier for each user
#   - item_id: unique identifier for each item
#   - rating: the rating given by the user to the item
#   - feature1: feature1 of the item
#   - feature2: feature2 of the item
#   - feature3: feature3 of the item
#   - feature4: feature4 of the item
#   - feature5: feature5 of the item

data = {'user_id': [1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5],
        'item_id': [101, 102, 103, 104, 101, 105, 101, 102, 103, 106, 101, 102, 101, 103],
        'rating': [4, 3, 5, 4, 4, 3, 3, 4, 5, 4, 5, 4, 4, 3],
        'feature1': ['feature1_item101', 'feature1_item102', 'feature1_item103', 'feature1_item104',
                     'feature1_item101', 'feature1_item105', 'feature1_item101', 'feature1_item102', 'feature1_item103', 'feature1_item106',
                     'feature1_item101', 'feature1_item102', 'feature1_item101', 'feature1_item103'],
        'feature2': ['feature2_item101', 'feature2_item102', 'feature2_item103', 'feature2_item104',
                     'feature2_item101', 'feature2_item105', 'feature2_item101', 'feature2_item102', 'feature2_item103', 'feature2_item106',
                     'feature2_item101', 'feature2_item102', 'feature2_item101', 'feature2_item103'],
        'feature3': ['feature3_item101', 'feature3_item102', 'feature3_item103', 'feature3_item104',
                     'feature3_item101', 'feature3_item105', 'feature3_item101', 'feature3_item102', 'feature3_item103', 'feature3_item106',
                     'feature3_item101', 'feature3_item102', 'feature3_item101', 'feature3_item103'],
        'feature4': ['feature4_item101', 'feature4_item102', 'feature4_item103', 'feature4_item104',
                     'feature4_item101', 'feature4_item105', 'feature4_item101', 'feature4_item102', 'feature4_item103', 'feature4_item106',
                     'feature4_item101', 'feature4_item102', 'feature4_item101', 'feature4_item103'],
        'feature5': ['feature5_item101', 'feature5_item102', 'feature5_item103', 'feature5_item104',
                     'feature5_item101', 'feature5_item105', 'feature5_item101', 'feature5_item102', 'feature5_item103', 'feature5_item106',
                     'feature5_item101', 'feature5_item102', 'feature5_item101', 'feature5_item103']}

df = pd.DataFrame(data)

# Convert the text features into numerical features using TF-IDF
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(df['feature1'] + df['feature2'] + df['feature3'] + df['feature4'] + df['feature5'])

# Use a LabelEncoder to convert the categorical variables into numerical variables
le = LabelEncoder()
df['item_id'] = le.fit_transform(df['item_id'])
df['user_id'] = le.fit_transform(df['user_id'])

# Split the data into training and testing sets
trainset = df[['user_id', 'item_id', 'rating']]
trainset, testset = train_test_split(trainset, test_size=0.2, random_state=42)

# Create a Surprise Reader object
reader = Reader(rating_scale=(1, 5))

# Create a Surprise Dataset from the training data
data = Dataset.load_from_df(trainset[['user_id', 'item_id', 'rating']], reader)

# Split the data into training and testing sets for Surprise
trainset = data.build_full_trainset()
trainset = trainset.build_testset()

# Create a Surprise SVD model
algo = SVD()

# Train the model
algo.fit(trainset)

# Make predictions on the test set
predictions = algo.test(trainset)

# Evaluate the model
print("SVD evaluation:")
print("MSE:", np.mean([p.est - p.rui**2 for p in predictions]))
print("MAE:", np.mean([abs(p.est - p.rui) for p in predictions]))

# Use the trained model to make recommendations for a specific user
user_id = 0  # Replace with the user ID you want to make recommendations for
item_id = le.transform(['item101'])  # Replace with the item ID you want to check against

# Check if the user has rated the item before
if user_id in trainset.all_ratings()[item_id]:
    print(f"User {user_id} has rated item {item_id} before.")
else:
    # Use the trained model to predict the rating for the user and item
    prediction = algo.predict(user_id, item_id, r_ui=0, verbose=False)
    
    print(f"Predicted rating for user {user_id} and item {item_id}: {prediction.est}")

# Save the trained model to a file
with open('svd_model.pkl', 'wb') as f:
    pickle.dump(algo, f)

# Load the saved model
with open('svd_model.pkl', 'rb') as f:
    loaded_algo = pickle.load(f)

# Use the loaded model to make predictions
loaded_algo.fit(trainset)
loaded_predictions = loaded_algo.test(trainset)

# Evaluate the loaded model
print("Loaded SVD evaluation:")
print("MSE:", np.mean([p.est - p.rui**2 for p in loaded_predictions]))
print("MAE:", np.mean([abs(p.est - p.rui) for p in loaded_predictions]))