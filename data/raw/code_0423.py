"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Set seed for reproducibility
np.random.seed(0)

# Generate sample historical sales data (replace with your actual data)
np.random.seed(0)
num_samples = 100  # Number of data points
t = np.arange(num_samples)  # Time points
sales = np.random.normal(100, 10, num_samples) + 0.1 * t  # Simulated sales data

# Create a pandas DataFrame
df = pd.DataFrame({'Date': t, 'Sales': sales})

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# Plot the original sales data
plt.figure(figsize=(10, 6))
plt.plot(df['Sales'], label='Original')
plt.legend(loc='best')
plt.title('Original Sales Data')
plt.show()

# Perform ADF test to check for stationarity
result = adfuller(df['Sales'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])

# If p-value is less than 0.05, the time series is stationary
if result[1] < 0.05:
    print('The time series is stationary.')
else:
    print('The time series is non-stationary.')

# Plot the autocorrelation and partial autocorrelation function
plt.figure(figsize=(10, 6))
plot_acf(df['Sales'], lags=20)
plt.title('Autocorrelation Function')
plt.show()

plt.figure(figsize=(10, 6))
plot_pacf(df['Sales'], lags=20)
plt.title('Partial Autocorrelation Function')
plt.show()

# Perform decomposition to identify trends, seasonality, and residuals
decomposition = seasonal_decompose(df['Sales'], model='additive')
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
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# Fit an ARIMA model to the data
model = ARIMA(df['Sales'], order=(1,1,1))  # Order: (p, d, q)
model_fit = model.fit(disp=0)

# Print summary of the model
print(model_fit.summary())

# Plot the residuals to check for normality
residuals = pd.DataFrame(model_fit.resid)
plt.figure(figsize=(10, 6))
plt.plot(residuals)
plt.title('Residuals')
plt.show()

# Make predictions using the ARIMA model
forecast_steps = 30  # Number of forecast steps
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Plot the forecasted sales
plt.figure(figsize=(10, 6))
plt.plot(df['Sales'], label='Original')
plt.plot(np.arange(len(df['Sales']), len(df['Sales']) + forecast_steps), forecast, color='red', label='Forecast')
plt.fill_between(np.arange(len(df['Sales']), len(df['Sales']) + forecast_steps), conf_int[:, 0], conf_int[:, 1], color='pink', alpha=0.3)
plt.legend(loc='best')
plt.title('Forecasted Sales')
plt.show()

# Evaluate the model using mean squared error
mse = mean_squared_error(df['Sales'], model_fit.fittedvalues)
print('Mean Squared Error:', mse)