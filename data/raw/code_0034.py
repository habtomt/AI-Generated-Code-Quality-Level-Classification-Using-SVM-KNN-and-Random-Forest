#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def generate_price_demand_data(n=1000):
    np.random.seed(42)

    df = pd.DataFrame({
        "price": np.random.uniform(5, 100, n),
        "marketing_spend": np.random.normal(5000, 1200, n).clip(500, 20000),
        "seasonality": np.random.choice([0.8, 1.0, 1.2, 1.5], n),
        "competitor_price": np.random.uniform(5, 100, n),
    })

    noise = np.random.normal(0, 20, n)

    df["demand"] = (
        500
        - 3.5 * df["price"]
        + 0.02 * df["marketing_spend"]
        + 50 * df["seasonality"]
        + 1.5 * (df["competitor_price"] - df["price"])
        + noise
    ).clip(1)

    df["revenue"] = df["price"] * df["demand"]

    return df


def train_demand_model(df):
    features = ["price", "marketing_spend", "seasonality", "competitor_price"]
    X = df[features]
    y = df["demand"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    preds = model.predict(X_scaled)
    mse = mean_squared_error(y, preds)

    print("=== DEMAND MODEL ===")
    print(f"MSE: {mse:.2f}")

    return model, scaler


def simulate_dynamic_pricing(df, model, scaler):
    prices = np.linspace(df["price"].min(), df["price"].max(), 50)

    avg_marketing = df["marketing_spend"].mean()
    avg_seasonality = df["seasonality"].mean()
    avg_competitor = df["competitor_price"].mean()

    revenues = []

    for p in prices:
        X = np.array([[p, avg_marketing, avg_seasonality, avg_competitor]])
        X_scaled = scaler.transform(X)
        demand_pred = model.predict(X_scaled)[0]
        revenue = p * demand_pred
        revenues.append(revenue)

    best_idx = np.argmax(revenues)
    best_price = prices[best_idx]
    best_revenue = revenues[best_idx]

    print("\n=== DYNAMIC PRICING RESULT ===")
    print(f"Optimal Price: {best_price:.2f}")
    print(f"Expected Revenue: {best_revenue:.2f}")

    plt.figure()
    plt.plot(prices, revenues)
    plt.scatter(best_price, best_revenue, color="red")
    plt.title("Price vs Predicted Revenue")
    plt.xlabel("Price")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()


def analyze_relationship(df):
    plt.figure()
    plt.scatter(df["price"], df["demand"], alpha=0.5)
    plt.title("Price vs Demand")
    plt.xlabel("Price")
    plt.ylabel("Demand")
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.scatter(df["price"], df["revenue"], alpha=0.5)
    plt.title("Price vs Revenue")
    plt.xlabel("Price")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()


def main():
    df = generate_price_demand_data()

    train_demand_model(df)
    model, scaler = train_demand_model(df)

    analyze_relationship(df)
    simulate_dynamic_pricing(df, model, scaler)


if __name__ == "__main__":
    main()