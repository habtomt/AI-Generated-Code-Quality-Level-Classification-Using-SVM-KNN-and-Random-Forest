"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy import stats

# Load website traffic data (replace with your own data)
# For demonstration purposes, we'll use a sample dataset
data = {
    'Date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05'],
    'Page Views': [100, 120, 110, 130, 140],
    'Unique Visitors': [50, 60, 55, 65, 70],
    'Average Session Duration': [30, 40, 35, 45, 50],
    'Bounce Rate': [20, 30, 25, 35, 40],
    'Age (Years)': [25, 30, 28, 32, 29],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male']
}

# Load data into a pandas DataFrame
df = pd.DataFrame(data)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' column as the index
df.set_index('Date', inplace=True)

# Plot visitor behavior over time
plt.figure(figsize=(10, 6))
sns.lineplot(data=df[['Page Views', 'Unique Visitors', 'Average Session Duration']])
plt.title('Visitor Behavior Over Time')
plt.xlabel('Date')
plt.ylabel('Metric')
plt.legend(title='Metric')
plt.show()

# Calculate peak traffic times (morning, afternoon, evening)
peak_traffic_times = df['Page Views'].groupby(df.index.hour).mean().reset_index()
plt.figure(figsize=(8, 6))
sns.barplot(data=peak_traffic_times, x='hour', y='Page Views')
plt.title('Peak Traffic Times')
plt.xlabel('Hour')
plt.ylabel('Page Views')
plt.show()

# Identify user demographics (age, gender)
demographics = df[['Age (Years)', 'Gender']]
# Calculate mean and standard deviation of age
age_mean = demographics['Age (Years)'].mean()
age_std = demographics['Age (Years)'].std()
print(f'Mean Age: {age_mean:.2f} years')
print(f'Standard Deviation of Age: {age_std:.2f} years')

# Create a histogram of age distribution
plt.figure(figsize=(8, 6))
sns.histplot(data=demographics['Age (Years)'], kde=True)
plt.title('Age Distribution')
plt.xlabel('Age (Years)')
plt.ylabel('Frequency')
plt.show()

# Identify user demographics (gender)
gender_counts = demographics['Gender'].value_counts()
print('User Demographics (Gender):')
print(gender_counts)

# Calculate engagement metrics (bounce rate, average session duration)
engagement_metrics = df[['Bounce Rate', 'Average Session Duration']]
# Calculate mean and standard deviation of bounce rate and average session duration
bounce_rate_mean = engagement_metrics['Bounce Rate'].mean()
bounce_rate_std = engagement_metrics['Bounce Rate'].std()
average_session_duration_mean = engagement_metrics['Average Session Duration'].mean()
average_session_duration_std = engagement_metrics['Average Session Duration'].std()
print(f'Mean Bounce Rate: {bounce_rate_mean:.2f}%')
print(f'Standard Deviation of Bounce Rate: {bounce_rate_std:.2f}%')
print(f'Mean Average Session Duration: {average_session_duration_mean:.2f} minutes')
print(f'Standard Deviation of Average Session Duration: {average_session_duration_std:.2f} minutes')

# Create a scatter plot of bounce rate vs. average session duration
plt.figure(figsize=(8, 6))
sns.scatterplot(data=engagement_metrics, x='Bounce Rate', y='Average Session Duration')
plt.title('Bounce Rate vs. Average Session Duration')
plt.xlabel('Bounce Rate (%)')
plt.ylabel('Average Session Duration (minutes)')
plt.show()

# Use PCA to reduce dimensionality of user demographics (age, gender)
scaler = StandardScaler()
demographics_scaled = scaler.fit_transform(demographics)

pca = PCA(n_components=2)
demographics_pca = pca.fit_transform(demographics_scaled)

# Use KMeans clustering to identify user segments
kmeans = KMeans(n_clusters=3)
user_segments = kmeans.fit_predict(demographics_pca)

# Print cluster labels
print('User Segments:')
print(user_segments)

# Create a scatter plot of user segments
plt.figure(figsize=(8, 6))
sns.scatterplot(data=demographics_pca, x=0, y=1, hue=user_segments)
plt.title('User Segments')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()