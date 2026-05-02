import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
data = {
    'CustomerID': range(1, 201),
    'Age': np.random.randint(18, 70, 200),
    'AnnualIncome': np.random.randint(20000, 120000, 200),
    'SpendingScore': np.random.randint(1, 101, 200)
}
df = pd.DataFrame(data)

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[['Age', 'AnnualIncome', 'SpendingScore']])

kmeans = KMeans(n_init=10, n_clusters=4, random_state=42)
df['Cluster'] = kmeans.fit_predict(scaled_data)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='AnnualIncome', y='SpendingScore', hue='Cluster', palette='bright')
plt.title('Customer Segments')
plt.show()

print(df.groupby('Cluster').mean())