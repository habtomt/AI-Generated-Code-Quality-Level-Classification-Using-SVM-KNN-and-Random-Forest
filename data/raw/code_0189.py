import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def website_traffic_analysis():
    np.random.seed(42)
    times = pd.date_range("2023-01-01", periods=168, freq="H")
    traffic = np.random.poisson(lam=50, size=168) + (np.sin(np.linspace(0, 4 * np.pi, 168)) * 20)
    df = pd.DataFrame({'Timestamp': times, 'Visits': traffic})
    df['Hour'] = df['Timestamp'].dt.hour
    df['Day'] = df['Timestamp'].dt.day_name()
    
    peak_hours = df.groupby('Hour')['Visits'].mean()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Hour', y='Visits', ci=None)
    plt.title('Average Traffic by Hour of Day')
    plt.show()
    
    print("Peak Traffic Hour:", peak_hours.idxmax())
    print(df.describe())

if __name__ == "__main__":
    website_traffic_analysis()
