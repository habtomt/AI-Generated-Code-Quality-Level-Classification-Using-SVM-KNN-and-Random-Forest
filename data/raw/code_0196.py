import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations():
    data = {
        'User': ['A', 'A', 'B', 'B', 'C', 'C', 'D'],
        'Item': ['Laptop', 'Mouse', 'Laptop', 'Monitor', 'Mouse', 'Keyboard', 'Monitor'],
        'Rating': [5, 4, 4, 5, 2, 5, 4]
    }
    df = pd.DataFrame(data)
    matrix = df.pivot_table(index='User', columns='Item', values='Rating').fillna(0)
    
    user_sim = cosine_similarity(matrix)
    user_sim_df = pd.DataFrame(user_sim, index=matrix.index, columns=matrix.index)
    
    target_user = 'A'
    similar_users = user_sim_df[target_user].sort_values(ascending=False).index[1:3]
    
    recommended_items = matrix.loc[similar_users].mean().sort_values(ascending=False)
    already_bought = matrix.loc[target_user] > 0
    
    suggestions = recommended_items[~already_bought].index.tolist()
    return suggestions

if __name__ == "__main__":
    print(f"Personalized Suggestions: {get_recommendations()}")