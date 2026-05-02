#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def generate_synthetic_data(n_samples=500):
    np.random.seed(42)

    age = np.random.randint(18, 70, n_samples)
    income = np.random.randint(20000, 120000, n_samples)
    spending_score = np.random.randint(1, 100, n_samples)
    visit_frequency = np.random.randint(1, 30, n_samples)

    data = pd.DataFrame({
        "Age": age,
        "Income": income,
        "SpendingScore": spending_score,
        "VisitFrequency": visit_frequency
    })

    return data


def preprocess_data(df):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    return scaled_data, scaler


def find_optimal_k(data, max_k=10):
    inertia = []
    k_range = range(1, max_k + 1)

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(data)
        inertia.append(model.inertia_)

    plt.figure()
    plt.plot(k_range, inertia, marker='o')
    plt.title("Elbow Method for Optimal K")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.show()


def apply_kmeans(data, k=4):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data)
    return labels, kmeans


def visualize_clusters(data, labels):
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)

    plt.figure()
    scatter = plt.scatter(
        reduced_data[:, 0],
        reduced_data[:, 1],
        c=labels,
        cmap='viridis',
        alpha=0.7
    )

    plt.title("Customer Segments (PCA Projection)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.colorbar(scatter)
    plt.show()


def main():
    df = generate_synthetic_data()

    features = df[["Age", "Income", "SpendingScore", "VisitFrequency"]]
    scaled_data, _ = preprocess_data(features)

    find_optimal_k(scaled_data, max_k=10)

    labels, _ = apply_kmeans(scaled_data, k=4)

    df["Cluster"] = labels

    visualize_clusters(scaled_data, labels)

    print(df.groupby("Cluster").mean())


if __name__ == "__main__":
    main()