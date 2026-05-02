#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


def generate_synthetic_customers(n=500):
    np.random.seed(42)

    df = pd.DataFrame({
        "age": np.random.randint(18, 70, n),
        "annual_income": np.random.normal(50000, 15000, n).clip(20000, 120000),
        "spending_score": np.random.normal(50, 25, n).clip(1, 100),
        "visits_per_month": np.random.poisson(5, n),
        "avg_order_value": np.random.normal(80, 30, n).clip(10, 300)
    })

    return df


def load_data():
    try:
        df = pd.read_csv("customers.csv")
    except FileNotFoundError:
        df = generate_synthetic_customers()
    return df


def preprocess(df):
    scaler = StandardScaler()
    X = scaler.fit_transform(df)
    return X, scaler


def find_best_k(X):
    scores = []
    k_range = range(2, 10)

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X)
        score = silhouette_score(X, labels)
        scores.append(score)

    best_k = k_range[np.argmax(scores)]
    return best_k, scores


def train_kmeans(X, k):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X)
    return model, labels


def visualize_clusters(X, labels):
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(X)

    plt.figure()
    plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="viridis", s=30)
    plt.title("Customer Segments (PCA Reduced)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.tight_layout()
    plt.show()


def analyze_clusters(df, labels):
    df = df.copy()
    df["cluster"] = labels

    summary = df.groupby("cluster").mean()
    print(summary)


def main():
    df = load_data()

    X, scaler = preprocess(df)

    best_k, scores = find_best_k(X)

    model, labels = train_kmeans(X, best_k)

    visualize_clusters(X, labels)

    analyze_clusters(df, labels)


if __name__ == "__main__":
    main()