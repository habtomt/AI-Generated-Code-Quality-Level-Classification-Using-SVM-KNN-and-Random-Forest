"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime

# Load historical sales data
# Replace 'data.csv' with your actual data file
data = pd.read_csv('data.csv')

# Convert date column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Ensure date is in the correct order
data.sort_values(by='date', inplace=True)

# Set date as the index
data.set_index('date', inplace=True)

# Plot historical sales data
plt.figure(figsize=(10,6))
plt.plot(data['sales'], label='Historical Sales')
plt.title('Historical Sales Trend')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

# Prepare data for time series analysis
data['sales'] = pd.to_numeric(data['sales'])

# Simple Exponential Smoothing (SES)
ses_model = SimpleExpSmoothing(data['sales'])
ses_model_fit = ses_model.fit()
print('Simple Exponential Smoothing (SES) Model Parameters:')
print(ses_model_fit.params)

# Exponential Smoothing (ES)
es_model = ExponentialSmoothing(data['sales'])
es_model_fit = es_model.fit()
print('Exponential Smoothing (ES) Model Parameters:')
print(es_model_fit.params)

# ARIMA Model
arima_model = ARIMA(data['sales'], order=(1,1,1))  # Order: (p, d, q)
arima_model_fit = arima_model.fit(disp=-1)
print('ARIMA Model Parameters:')
print(arima_model_fit.summary())

# Plot residuals for ARIMA model
residuals = arima_model_fit.resid
plt.figure(figsize=(10,6))
plt.plot(residuals, label='Residuals')
plt.title('ARIMA Model Residuals')
plt.xlabel('Date')
plt.ylabel('Residual Value')
plt.legend()
plt.show()

# Evaluate ARIMA model using Mean Squared Error (MSE)
mse = mean_squared_error(data['sales'].iloc[-12:], arima_model_fit.forecast(steps=12)[0])
print(f'Mean Squared Error (MSE) for ARIMA Model: {mse}')

# Forecast future sales using ARIMA model
forecast_steps = 24  # Number of steps to forecast
forecast, stderr, conf_int = arima_model_fit.forecast(steps=forecast_steps)
print(f'Forecasted Sales for Next {forecast_steps} Steps:')
print(forecast)

# Plot forecasted sales
plt.figure(figsize=(10,6))
plt.plot(data['sales'], label='Historical Sales')
plt.plot(np.arange(len(data['sales']), len(data['sales'])+forecast_steps), forecast, label='Forecasted Sales', linestyle='--', color='r')
plt.title('Forecasted Sales Trend')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

# Save forecasted sales to a new CSV file
forecast_df = pd.DataFrame(forecast, index=pd.date_range(start=data.index[-1]+pd.DateOffset(months=1), periods=forecast_steps, freq='MS'), columns=['forecasted_sales'])
forecast_df.to_csv('forecasted_sales.csv')