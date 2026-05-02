"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

# Set seed for reproducibility
np.random.seed(0)

# Generate sample sales data (replace with real data)
np.random.seed(0)
days = 365
sales_data = np.random.randint(1, 100, size=days)
dates = pd.date_range('2022-01-01', periods=days)

# Create a pandas DataFrame
df = pd.DataFrame({'Date': dates, 'Sales': sales_data})

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Plot original sales data
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Sales'], label='Original Sales Data')
plt.title('Original Sales Data')
plt.legend()
plt.show()

# Decompose sales data to identify trends and seasonality
decomposition = seasonal_decompose(df['Sales'], model='additive')

# Plot decomposed components
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.figure(figsize=(10, 6))
plt.subplot(411)
plt.plot(df['Sales'], label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# Perform ADF test to check for stationarity
result = adfuller(df['Sales'])

# Print ADF test results
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:')
for key, value in result[4].items():
    print(key, ':', value)

# If ADF test indicates non-stationarity, perform differencing
if result[1] > 0.05:
    df_diff = df['Sales'].diff().dropna()
    print('Differenced Sales Data:')
    print(df_diff)

# Plot ACF and PACF plots to determine order of differencing
plot_acf(df_diff, lags=30)
plot_pacf(df_diff, lags=30)
plt.show()

# Determine order of differencing (k) using ACF and PACF plots
k = 1  # based on ACF and PACF plots

# Perform k times differencing
df_diff_k = df['Sales'].diff(k).dropna()
print('Differenced Sales Data (k times):')
print(df_diff_k)

# Split data into training and testing sets
train_data, test_data = train_test_split(df_diff_k, test_size=0.2, random_state=42)

# Scale data using StandardScaler
scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_data.values.reshape(-1, 1))
test_scaled = scaler.transform(test_data.values.reshape(-1, 1))

# Create a Linear Regression model
model = LinearRegression()

# Train the model on the scaled training data
model.fit(train_scaled, train_data.values)

# Make predictions on the scaled testing data
predictions = model.predict(test_scaled)

# Plot predicted vs actual sales data
plt.figure(figsize=(10, 6))
plt.plot(test_data.index, test_data.values, label='Actual')
plt.plot(test_data.index, predictions, label='Predicted')
plt.title('Predicted vs Actual Sales Data')
plt.legend()
plt.show()