"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# Generate sample customer data (replace with actual data)
np.random.seed(0)
customer_data = {
    'Age': np.random.randint(18, 80, 100),
    'Income': np.random.randint(30000, 150000, 100),
    'Purchases': np.random.randint(0, 100, 100),
    'Gender': np.random.choice(['Male', 'Female'], 100),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
}

# Create a DataFrame from the generated data
df = pd.DataFrame(customer_data)

# One-hot encode categorical variables
df = pd.get_dummies(df, columns=['Gender', 'Region'])

# Define features (X) and target variable (y)
X = df.drop('Purchases', axis=1)
y = df['Purchases']

# Scale the data using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA to reduce dimensionality (optional)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Try different number of clusters (k) and choose the best one using silhouette score
silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_pca)
    score = silhouette_score(X_pca, kmeans.labels_)
    silhouette_scores.append(score)
    print(f'k={k}, Silhouette Score: {score}')

# Choose the best value of k
best_k = np.argmax(silhouette_scores) + 2  # Add 2 to get the actual value of k
print(f'Best k: {best_k}')

# Perform K-means clustering with the best value of k
kmeans = KMeans(n_clusters=best_k)
kmeans.fit(X_pca)

# Plot the clusters
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_)
plt.title('Customer Clusters')
plt.show()

# Evaluate the clustering using Calinski-Harabasz index
score = calinski_harabasz_score(X_pca, kmeans.labels_)
print(f'Calinski-Harabasz Score: {score}')