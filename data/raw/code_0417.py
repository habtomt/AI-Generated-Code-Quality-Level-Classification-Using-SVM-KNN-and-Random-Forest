"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.datasets import make_blobs

# Create a sample dataset for customer data
np.random.seed(0)
X, y = make_blobs(n_samples=200, centers=5, n_features=4, random_state=0)
df = pd.DataFrame(X, columns=['Age', 'Income', 'Spending', 'Savings'])

# Replace placeholder credentials with real API keys if necessary
# api_key = 'YOUR_API_KEY'

# Standardize the features
scaler = StandardScaler()
df_stand = scaler.fit_transform(df)

# Apply KMeans clustering to find key segments
kmeans = KMeans(n_clusters=5, random_state=0)
kmeans.fit(df_stand)
labels = kmeans.labels_

# Evaluate the clustering using silhouette score
silhouette_score = metrics.silhouette_score(df_stand, labels)
print(f'Silhouette Score: {silhouette_score}')

# Perform PCA to reduce dimensionality and visualize the clusters
pca = PCA(n_components=2)
pca_df = pca.fit_transform(df_stand)
pca_df = pd.DataFrame(pca_df, columns=['Principal Component 1', 'Principal Component 2'])

# Visualize the clusters
plt.figure(figsize=(8, 6))
plt.scatter(pca_df['Principal Component 1'], pca_df['Principal Component 2'], c=labels)
plt.title('Customer Segments')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# Group the data by cluster labels and calculate the mean of each feature
grouped_df = df_stand.groupby(labels).mean()
print(grouped_df)