"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_000.txt
Run      : 1
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

def load_data(file_path, date_column, sales_column):
    """Load sales data from a CSV file."""
    try:
        data = pd.read_csv(file_path, parse_dates=[date_column])
        data.set_index(date_column, inplace=True)
        return data[sales_column]
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def explore_data(data):
    """Explore the sales data."""
    print(data.head())
    print(data.describe())

def visualize_sales(data):
    """Visualize sales data over time."""
    plt.figure(figsize=(10, 6))
    plt.plot(data, label='Sales')
    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

def check_stationarity(data):
    """Check if the time series is stationary using the Augmented Dickey-Fuller Test."""
    result = adfuller(data)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    if result[1] > 0.05:
        print('The time series is not stationary.')
    else:
        print('The time series is stationary.')

def decompose_time_series(data):
    """Decompose the time series into trend, seasonal, and residual components."""
    decomposition = seasonal_decompose(data, model='additive')
    fig = decomposition.plot()
    fig.set_size_inches(10, 8)
    plt.show()
    return decomposition

def plot_components(decomposition, data):
    """Plot each component of the time series."""
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.figure(figsize=(12, 8))
    plt.subplot(411)
    plt.plot(data, label='Original', color='blue')
    plt.legend(loc='upper left')
    plt.subplot(412)
    plt.plot(trend, label='Trend', color='orange')
    plt.legend(loc='upper left')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality', color='green')
    plt.legend(loc='upper left')
    plt.subplot(414)
    plt.plot(residual, label='Residuals', color='red')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

def build_arima_model(data):
    """Build an ARIMA model for forecasting."""
    data_diff = data.diff().dropna()
    model = ARIMA(data_diff, order=(1, 1, 1))
    fit_model = model.fit()
    print(fit_model.summary())
    forecast = fit_model.forecast(steps=12)
    print(forecast)

def main():
    file_path = 'sales_data.csv'  # replace with your file path
    date_column = 'date_column'  # replace with your date column
    sales_column = 'sales_column'  # replace with your sales column

    data = load_data(file_path, date_column, sales_column)
    if data is not None:
        explore_data(data)
        visualize_sales(data)
        check_stationarity(data)
        decomposition = decompose_time_series(data)
        plot_components(decomposition, data)
        build_arima_model(data)

if __name__ == "__main__":
    main()