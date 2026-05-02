import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def customer_segmentation():
    np.random.seed(42)
    data = {
        'CustomerID': range(1, 101),
        'Age': np.random.randint(18, 70, 100),
        'AnnualIncome': np.random.randint(20, 120, 100),
        'SpendingScore': np.random.randint(1, 100, 100)
    }
    df = pd.DataFrame(data)
    
    features = df[['Age', 'AnnualIncome', 'SpendingScore']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df['Segment'] = kmeans.fit_predict(scaled_features)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='AnnualIncome', y='SpendingScore', hue='Segment', palette='viridis')
    plt.title('Customer Segments')
    plt.show()
    
    print(df.groupby('Segment').mean())

if __name__ == "__main__":
    customer_segmentation()
