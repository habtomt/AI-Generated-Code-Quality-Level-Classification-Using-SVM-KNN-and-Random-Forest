import pandas as pd
import numpy as np

data = {
    'Station': ['Assembly', 'Assembly', 'Testing', 'Testing', 'Packing', 'Packing'],
    'ProcessTime': [45, 50, 120, 115, 30, 25],
    'Capacity': [60, 60, 60, 60, 60, 60]
}

df = pd.DataFrame(data)
analysis = df.groupby('Station')['ProcessTime'].mean().reset_index()
analysis['Utilization'] = analysis['ProcessTime'] / 60

bottleneck = analysis.loc[analysis['ProcessTime'].idxmax()]

print(analysis)
print("\nCritical Bottleneck:")
print(bottleneck)