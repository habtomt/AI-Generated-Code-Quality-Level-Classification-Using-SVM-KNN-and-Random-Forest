import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Synthetic user-product data
# -----------------------------
np.random.seed(42)

users = [f"U{i}" for i in range(1, 11)]
products = [f"P{i}" for i in range(1, 11)]

data = []
for u in users:
    for p in products:
        rating = np.random.randint(0, 6)  # 0 means no interaction
        if rating > 0:
            data.append([u, p, rating])

df = pd.DataFrame(data, columns=["user", "product", "rating"])

# -----------------------------
# Create user-item matrix
# -----------------------------
user_item_matrix = df.pivot_table(index="user", columns="product", values="rating").fillna(0)

# -----------------------------
# Item-based collaborative filtering
# -----------------------------
item_similarity = cosine_similarity(user_item_matrix.T)
item_similarity_df = pd.DataFrame(item_similarity, index=products, columns=products)

# -----------------------------
# Recommendation function
# -----------------------------
def recommend_products(user_id, top_n=5):
    if user_id not in user_item_matrix.index:
        return []

    user_ratings = user_item_matrix.loc[user_id]
    scores = {}

    for product in products:
        if user_ratings[product] == 0:
            sim_scores = item_similarity_df[product]
            weighted_sum = np.dot(sim_scores, user_ratings)
            sim_sum = np.sum(np.abs(sim_scores))

            if sim_sum > 0:
                scores[product] = weighted_sum / sim_sum

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    test_user = "U1"
    recommendations = recommend_products(test_user)

    print(f"Recommendations for {test_user}:")
    for product, score in recommendations:
        print(f"{product} -> {score:.4f}")