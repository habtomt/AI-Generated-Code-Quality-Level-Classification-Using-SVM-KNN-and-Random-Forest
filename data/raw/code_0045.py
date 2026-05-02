#!/usr/bin/env python3

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def generate_synthetic_data():
    users = [f"U{i}" for i in range(1, 11)]
    items = [f"P{i}" for i in range(1, 11)]

    np.random.seed(42)
    data = []

    for u in users:
        for i in items:
            rating = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.3, 0.1, 0.1, 0.2, 0.2, 0.1])
            if rating > 0:
                data.append([u, i, rating])

    return pd.DataFrame(data, columns=["user", "item", "rating"])


def create_user_item_matrix(df):
    matrix = df.pivot_table(index="user", columns="item", values="rating").fillna(0)
    return matrix


def compute_similarity(matrix):
    sim = cosine_similarity(matrix)
    return pd.DataFrame(sim, index=matrix.index, columns=matrix.index)


def recommend(user, matrix, similarity, top_n=3):
    if user not in matrix.index:
        return []

    user_scores = similarity[user].drop(user)
    similar_users = user_scores.sort_values(ascending=False)

    weighted_scores = pd.Series(dtype=float)

    for other_user, weight in similar_users.items():
        weighted_scores = weighted_scores.add(matrix.loc[other_user] * weight, fill_value=0)

    seen_items = matrix.loc[user]
    weighted_scores = weighted_scores[seen_items == 0]

    return weighted_scores.sort_values(ascending=False).head(top_n)


def main():
    df = generate_synthetic_data()

    matrix = create_user_item_matrix(df)

    similarity = compute_similarity(matrix)

    user = "U1"
    recs = recommend(user, matrix, similarity)

    print(f"Recommendations for {user}:")
    print(recs)


if __name__ == "__main__":
    main()