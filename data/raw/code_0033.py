#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def generate_campaign_data(n=1000):
    np.random.seed(42)

    df = pd.DataFrame({
        "ad_spend": np.random.normal(5000, 1500, n).clip(500, 20000),
        "email_clicks": np.random.poisson(200, n),
        "social_media_engagement": np.random.normal(300, 100, n).clip(50, 1000),
        "website_visits": np.random.normal(1000, 300, n).clip(100, 5000),
        "discount_offered": np.random.choice([0, 5, 10, 15, 20], n),
    })

    noise = np.random.normal(0, 50, n)

    df["conversions"] = (
        0.002 * df["ad_spend"] +
        0.01 * df["email_clicks"] +
        0.005 * df["social_media_engagement"] +
        0.003 * df["website_visits"] +
        2 * df["discount_offered"] +
        noise
    ).clip(0)

    df["revenue"] = df["conversions"] * np.random.normal(100, 20, n)

    return df


def compute_kpis(df):
    conversion_rate = df["conversions"].sum() / df["website_visits"].sum()
    total_cost = df["ad_spend"].sum()
    total_revenue = df["revenue"].sum()
    roi = (total_revenue - total_cost) / total_cost

    engagement_score = (
        df["email_clicks"].mean()
        + df["social_media_engagement"].mean()
    )

    print("=== KPI REPORT ===")
    print(f"Conversion Rate: {conversion_rate:.4f}")
    print(f"ROI: {roi:.4f}")
    print(f"Engagement Score: {engagement_score:.2f}")


def correlation_analysis(df):
    corr = df.corr(numeric_only=True)

    plt.figure()
    plt.imshow(corr, cmap="coolwarm")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Feature Correlation Matrix")
    plt.tight_layout()
    plt.show()


def predict_conversions(df):
    features = [
        "ad_spend",
        "email_clicks",
        "social_media_engagement",
        "website_visits",
        "discount_offered",
    ]

    X = df[features]
    y = df["conversions"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    preds = model.predict(X_scaled)

    mse = mean_squared_error(y, preds)

    print("\n=== MODEL EVALUATION ===")
    print(f"Mean Squared Error: {mse:.2f}")

    plt.figure()
    plt.scatter(y, preds, alpha=0.5)
    plt.xlabel("Actual Conversions")
    plt.ylabel("Predicted Conversions")
    plt.title("Actual vs Predicted Conversions")
    plt.tight_layout()
    plt.show()


def campaign_impact_analysis(df):
    grouped = df.groupby("discount_offered")[["conversions", "revenue"]].mean()

    plt.figure()
    grouped["conversions"].plot(kind="bar")
    plt.title("Average Conversions by Discount Level")
    plt.tight_layout()
    plt.show()

    plt.figure()
    grouped["revenue"].plot(kind="bar")
    plt.title("Average Revenue by Discount Level")
    plt.tight_layout()
    plt.show()


def main():
    df = generate_campaign_data()

    compute_kpis(df)
    correlation_analysis(df)
    predict_conversions(df)
    campaign_impact_analysis(df)


if __name__ == "__main__":
    main()