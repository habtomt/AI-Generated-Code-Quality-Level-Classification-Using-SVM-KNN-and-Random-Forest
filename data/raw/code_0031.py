#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm

def generate_synthetic_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
    n = len(dates)

    df = pd.DataFrame({"date": dates})
    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
    df["holiday"] = np.random.binomial(1, 0.03, n)

    base = 200
    trend = np.linspace(0, 80, n)
    seasonality = 30 * np.sin(2 * np.pi * df["month"] / 12)
    weekly = 15 * np.sin(2 * np.pi * df["dayofweek"] / 7)

    price = 10 + np.random.normal(0, 1, n)
    marketing = np.random.normal(50, 10, n)

    noise = np.random.normal(0, 15, n)

    df["price"] = price
    df["marketing_spend"] = marketing

    df["sales"] = (
        base
        + trend
        + seasonality
        + weekly
        - 2 * price
        + 0.5 * marketing
        + 25 * df["holiday"]
        + 10 * df["is_weekend"]
        + noise
    )

    return df


def load_or_create_data():
    if os.path.exists("sales.csv"):
        df = pd.read_csv("sales.csv", parse_dates=["date"])
    else:
        df = generate_synthetic_data()
    return df


def plot_sales(df):
    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    plt.figure()
    plt.plot(df["sales"], label="Sales")
    plt.title("Sales Over Time")
    plt.legend()
    plt.tight_layout()
    plt.show()

    rolling = df["sales"].rolling(window=30).mean()
    plt.figure()
    plt.plot(df["sales"], alpha=0.4)
    plt.plot(rolling, label="30-Day Rolling Mean")
    plt.title("Trend Analysis")
    plt.legend()
    plt.tight_layout()
    plt.show()


def seasonal_analysis(df):
    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    decomposition = seasonal_decompose(df["sales"], model="additive", period=365)

    decomposition.plot()
    plt.tight_layout()
    plt.show()


def correlation_analysis(df):
    plt.figure()
    corr = df[["sales", "price", "marketing_spend", "holiday", "is_weekend"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.show()


def regression_analysis(df):
    features = ["price", "marketing_spend", "holiday", "is_weekend", "dayofweek", "month"]
    X = df[features]
    y = df["sales"]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    print(model.summary())


def main():
    df = load_or_create_data()

    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month

    plot_sales(df.copy())
    seasonal_analysis(df.copy())
    correlation_analysis(df.copy())
    regression_analysis(df)


if __name__ == "__main__":
    main()