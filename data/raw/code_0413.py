"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_001.txt
Run      : 1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_squared_error

def load_data(file_path):
    # Load the sales data
    try:
        data = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def visualize_data(data):
    # Plot the sales data
    plt.figure(figsize=(10, 6))
    plt.plot(data['sales'], label='Sales')
    plt.title('Sales Data')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

def decompose_time_series(data):
    # Decompose the time series
    decomposition = seasonal_decompose(data['sales'], model='additive')
    decomposition.plot()
    plt.show()

def split_data(data):
    # Split data into training and testing sets
    train_size = int(len(data) * 0.8)
    train, test = data.iloc[:train_size], data.iloc[train_size:]
    return train, test

def fit_sarima_model(train):
    # Fit a SARIMA model
    try:
        model = SARIMAX(train['sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit(disp=False)
        return model_fit
    except Exception as e:
        print(f"Failed to fit SARIMA model: {e}")
        return None

def forecast(model_fit, test):
    # Forecast
    forecast = model_fit.get_forecast(steps=len(test))
    forecast_index = test.index
    forecast_values = forecast.predicted_mean
    conf_int = forecast.conf_int()
    return forecast_index, forecast_values, conf_int

def visualize_forecast(data, forecast_index, forecast_values, conf_int):
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['sales'], label='Observed')
    plt.plot(forecast_index, forecast_values, color='red', label='Forecast')
    plt.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)
    plt.title('Sales Forecast')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

def evaluate_model(test, forecast_values):
    # Evaluate the model
    mse = mean_squared_error(test['sales'], forecast_values)
    print(f'Mean Squared Error: {mse:.2f}')

def main():
    file_path = 'sales_data.csv'  # Replace with your file path
    data = load_data(file_path)
    if data is not None:
        print(data.head())
        visualize_data(data)
        decompose_time_series(data)
        train, test = split_data(data)
        model_fit = fit_sarima_model(train)
        if model_fit is not None:
            forecast_index, forecast_values, conf_int = forecast(model_fit, test)
            visualize_forecast(data, forecast_index, forecast_values, conf_int)
            evaluate_model(test, forecast_values)

if __name__ == "__main__":
    main()