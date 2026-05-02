"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_000.txt
Run      : 1
"""

# Import necessary libraries
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D

def load_data(file_name):
    """Load customer data from a CSV file."""
    try:
        data = pd.read_csv(file_name)
        return data
    except FileNotFoundError:
        print("The file does not exist.")
        return None

def preprocess_data(data, features):
    """Preprocess the data by selecting relevant features and scaling them."""
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def determine_optimal_clusters(X_scaled):
    """Determine the optimal number of clusters using the Elbow Method."""
    inertia = []
    range_n_clusters = range(1, 11)
    for n_clusters in range_n_clusters:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)
    return inertia, range_n_clusters

def visualize_elbow_method(inertia, range_n_clusters):
    """Visualize the Elbow method."""
    plt.figure(figsize=(8, 5))
    plt.plot(range_n_clusters, inertia, marker='o', linestyle='-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.show()

def apply_kmeans_clustering(X_scaled, optimal_clusters):
    """Apply K-Means clustering."""
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    return labels

def visualize_clusters(data, labels):
    """Visualize the clusters."""
    data['Cluster'] = labels
    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=data, x='Age', y='SpendingScore', hue='Cluster', palette='viridis', style='Cluster')
    plt.title('Customer Segments')
    plt.xlabel('Age')
    plt.ylabel('Spending Score')
    plt.legend(title='Cluster')
    plt.show()

def visualize_3d_clusters(data):
    """Visualize the clusters in 3D."""
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(data['Age'], data['Income'], data['SpendingScore'],
                         c=data['Cluster'], cmap='viridis')

    ax.set_title('3D view of Customer Segments')
    ax.set_xlabel('Age')
    ax.set_ylabel('Income')
    ax.set_zlabel('Spending Score')
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)
    plt.show()

def main():
    # Load the dataset
    file_name = 'customer_data.csv'
    data = load_data(file_name)

    if data is not None:
        # Preprocess the data
        features = ['Age', 'Income', 'SpendingScore']  
        X_scaled = preprocess_data(data, features)

        # Determine the optimal number of clusters
        inertia, range_n_clusters = determine_optimal_clusters(X_scaled)
        visualize_elbow_method(inertia, range_n_clusters)

        # Apply K-Means clustering
        optimal_clusters = 3
        labels = apply_kmeans_clustering(X_scaled, optimal_clusters)

        # Visualize the clusters
        visualize_clusters(data, labels)
        visualize_3d_clusters(data)

if __name__ == "__main__":
    main()