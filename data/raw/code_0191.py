import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_recommendations():
    data = {
        'User1': [5, 4, 0, 0, 1],
        'User2': [0, 0, 5, 4, 2],
        'User3': [4, 5, 0, 0, 2],
        'User4': [0, 0, 4, 5, 1]
    }
    products = ['Laptop', 'Smartphone', 'Gardening Tools', 'Outdoor Grill', 'Phone Case']
    df = pd.DataFrame(data, index=products).T
    
    similarity_matrix = cosine_similarity(df)
    similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)
    
    print("User Similarity Matrix:")
    print(similarity_df)
    
    def get_recommendations(user):
        similar_users = similarity_df[user].sort_values(ascending=False).index[1:]
        top_similar_user = similar_users[0]
        user_ratings = df.loc[user]
        similar_user_ratings = df.loc[top_similar_user]
        
        recommendations = similar_user_ratings[(user_ratings == 0) & (similar_user_ratings > 3)]
        return recommendations

    print("\nRecommendations for User1:")
    print(get_recommendations('User1'))

if __name__ == "__main__":
    build_recommendations()
