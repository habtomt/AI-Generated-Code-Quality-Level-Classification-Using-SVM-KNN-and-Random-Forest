"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Generate sample customer data
X, _ = make_classification(n_samples=1000, n_features=20, n_informative=10, n_redundant=5, random_state=42)

# Convert data to DataFrame
df = pd.DataFrame(X, columns=[f'Feature_{i}' for i in range(1, 21)])

# Print initial DataFrame shape
print("Initial DataFrame shape:", df.shape)

# Convert categorical features to numerical (if any)
# For simplicity, assume all features are numerical

# Scale features using StandardScaler
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Convert scaled data back to DataFrame
df_scaled = pd.DataFrame(df_scaled, columns=df.columns)

# Print scaled DataFrame shape
print("Scaled DataFrame shape:", df_scaled.shape)

# Use KMeans clustering algorithm
# Determine optimal number of clusters using silhouette score
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(df_scaled)
    score = silhouette_score(df_scaled, kmeans.labels_)
    print(f"Silhouette score for n_clusters={n_clusters}: {score}")

# Choose optimal number of clusters (e.g., n_clusters=5)
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(df_scaled)

# Get cluster labels
labels = kmeans.labels_

# Print cluster labels
print("Cluster labels:", labels)

# Visualize clusters using PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(df_scaled)
plt.scatter(pca_data[:, 0], pca_data[:, 1], c=labels)
plt.title("PCA Clustering")
plt.show()

# Visualize clusters using TSNE
tsne = TSNE(n_components=2, random_state=42)
tsne_data = tsne.fit_transform(df_scaled)
plt.scatter(tsne_data[:, 0], tsne_data[:, 1], c=labels)
plt.title("TSNE Clustering")
plt.show()

# Print cluster statistics (e.g., mean, count)
cluster_stats = df_scaled.groupby(labels).agg(['mean', 'count'])
print("Cluster statistics:")
print(cluster_stats)