#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA


def generate_synthetic_sales(n_periods=200):
    np.random.seed(42)
    time = np.arange(n_periods)

    trend = time * 0.5
    seasonality = 10 * np.sin(2 * np.pi * time / 12)
    noise = np.random.normal(0, 2, n_periods)

    sales = 50 + trend + seasonality + noise

    dates = pd.date_range(start="2020-01-01", periods=n_periods, freq="M")
    df = pd.DataFrame({"Date": dates, "Sales": sales})
    df.set_index("Date", inplace=True)

    return df


def plot_sales(df):
    plt.figure()
    plt.plot(df.index, df["Sales"])
    plt.title("Historical Sales Data")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.show()


def train_arima_model(series):
    model = ARIMA(series, order=(5, 1, 0))
    fitted_model = model.fit()
    return fitted_model


def forecast_sales(model, steps=24):
    forecast = model.forecast(steps=steps)
    return forecast


def plot_forecast(df, forecast):
    plt.figure()

    plt.plot(df.index, df["Sales"], label="Historical Sales")

    future_dates = pd.date_range(
        start=df.index[-1], periods=len(forecast) + 1, freq="M"
    )[1:]

    plt.plot(future_dates, forecast, label="Forecasted Sales", linestyle="--")

    plt.title("Sales Forecast")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend()
    plt.show()


def main():
    df = generate_synthetic_sales()

    plot_sales(df)

    model = train_arima_model(df["Sales"])

    forecast = forecast_sales(model, steps=24)

    plot_forecast(df, forecast)

    print(model.summary())


if __name__ == "__main__":
    main()