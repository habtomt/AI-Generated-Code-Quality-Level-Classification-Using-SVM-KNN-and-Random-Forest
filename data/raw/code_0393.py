"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Load sample customer data (replace with your own data)
data = {
    'Customer ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Age': [25, 32, 47, 28, 35, 42, 55, 38, 20, 45],
    'Income': [50000, 60000, 80000, 55000, 65000, 75000, 90000, 70000, 45000, 85000],
    'Gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'Purchased': [True, True, False, True, False, True, False, True, True, False],
    'Spent': [100, 200, 0, 150, 0, 250, 0, 180, 110, 0],
    'Visited': [5, 10, 3, 7, 1, 12, 2, 9, 6, 4]
}

df = pd.DataFrame(data)

# One-hot encoding for categorical variables
df = pd.get_dummies(df, columns=['Gender'])

# Drop unnecessary columns
df = df.drop(['Customer ID', 'Purchased'], axis=1)

# Replace boolean values with integers
df['Visited'] = df['Visited'].astype(int)

# Scale numerical features using StandardScaler
scaler = StandardScaler()
df[['Age', 'Income', 'Spent', 'Visited']] = scaler.fit_transform(df[['Age', 'Income', 'Spent', 'Visited']])

# Split data into features (X) and target variable (y)
X = df.drop('Spent', axis=1)
y = df['Spent']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Perform PCA to reduce dimensionality (optional)
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Determine the optimal number of clusters using the Silhouette Coefficient
silhouette_scores = []
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X_train_pca)
    score = silhouette_score(X_train_pca, kmeans.labels_)
    silhouette_scores.append(score)
    print(f'Number of clusters: {n_clusters}, Silhouette Coefficient: {score}')

# Choose the number of clusters with the highest Silhouette Coefficient
n_clusters = silhouette_scores.index(max(silhouette_scores)) + 2

# Perform K-means clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(X_train_pca)

# Get cluster labels for the training and testing sets
train_labels = kmeans.labels_
test_labels = kmeans.predict(X_test_pca)

# Print cluster labels for the testing set
print('Cluster labels for the testing set:')
print(test_labels)

# Save cluster labels to a file (optional)
# with open('cluster_labels.txt', 'w') as f:
#     f.write('\n'.join(map(str, test_labels)))