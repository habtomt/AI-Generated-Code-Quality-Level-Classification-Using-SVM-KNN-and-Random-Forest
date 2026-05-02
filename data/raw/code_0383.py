"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_001.txt
Run      : 1
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """Load customer data from a CSV file."""
    try:
        # Load your dataset
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def select_features(df, features):
    """Select features for clustering."""
    try:
        # Select the features for clustering
        X = df[features]
        return X
    except Exception as e:
        print(f"Error selecting features: {e}")
        return None

def standardize_data(X):
    """Standardize the data."""
    try:
        # Standardize the data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        return X_scaled
    except Exception as e:
        print(f"Error standardizing data: {e}")
        return None

def choose_clusters(X_scaled):
    """Choose the number of clusters using the Elbow method."""
    try:
        # Choose the number of clusters using the Elbow method
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
            kmeans.fit(X_scaled)
            wcss.append(kmeans.inertia_)
        
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, 11), wcss, marker='o')
        plt.title('Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()
        
        # From the elbow plot, choose an appropriate number of clusters
        n_clusters = int(input("Enter the number of clusters: "))
        return n_clusters
    except Exception as e:
        print(f"Error choosing clusters: {e}")
        return None

def fit_kmeans(X_scaled, n_clusters):
    """Fit KMeans."""
    try:
        # Fit KMeans
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
        return kmeans
    except Exception as e:
        print(f"Error fitting KMeans: {e}")
        return None

def visualize_clusters(df, features):
    """Visualize the clusters."""
    try:
        # Visualize the clusters
        plt.figure(figsize=(10, 7))
        sns.scatterplot(x=features[1], y=features[2], hue='Cluster', data=df, palette='viridis', s=60)
        plt.title('Customer Clusters')
        plt.show()
    except Exception as e:
        print(f"Error visualizing clusters: {e}")

def main():
    file_path = 'customer_data.csv'  # Replace with your file path
    features = ['Age', 'Annual Income', 'Spending Score']  # Add more features as needed
    
    # Load data
    df = load_data(file_path)
    
    if df is not None:
        # Select features
        X = select_features(df, features)
        
        if X is not None:
            # Standardize data
            X_scaled = standardize_data(X)
            
            if X_scaled is not None:
                # Choose clusters
                n_clusters = choose_clusters(X_scaled)
                
                if n_clusters is not None:
                    # Fit KMeans
                    kmeans = fit_kmeans(X_scaled, n_clusters)
                    
                    if kmeans is not None:
                        # Predict clusters
                        df['Cluster'] = kmeans.fit_predict(X_scaled)
                        
                        # Visualize clusters
                        visualize_clusters(df, features)

if __name__ == "__main__":
    main()