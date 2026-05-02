#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error


def generate_operational_data(n=1000):
    np.random.seed(42)

    df = pd.DataFrame({
        "process_time": np.random.normal(50, 10, n).clip(10, 120),
        "wait_time": np.random.normal(20, 8, n).clip(0, 60),
        "machine_utilization": np.random.uniform(0.4, 1.0, n),
        "labor_hours": np.random.normal(8, 2, n).clip(1, 16),
        "defect_rate": np.random.uniform(0, 0.1, n),
        "material_cost": np.random.normal(100, 20, n).clip(20, 300),
    })

    noise = np.random.normal(0, 5, n)

    df["output"] = (
        200
        - 1.2 * df["process_time"]
        - 0.8 * df["wait_time"]
        + 50 * df["machine_utilization"]
        + 2 * df["labor_hours"]
        - 300 * df["defect_rate"]
        - 0.5 * df["material_cost"]
        + noise
    ).clip(1)

    df["cost"] = (
        df["process_time"] * 2
        + df["wait_time"] * 1.5
        + df["labor_hours"] * 20
        + df["material_cost"]
    )

    return df


def train_model(df):
    features = [
        "process_time",
        "wait_time",
        "machine_utilization",
        "labor_hours",
        "defect_rate",
        "material_cost",
    ]

    X = df[features]
    y = df["output"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    preds = model.predict(X_scaled)
    mse = mean_squared_error(y, preds)

    print("=== MODEL PERFORMANCE ===")
    print(f"MSE: {mse:.2f}")

    return model, scaler, features


def feature_importance(model, features):
    importances = model.feature_importances_
    idx = np.argsort(importances)

    plt.figure()
    plt.barh(range(len(features)), importances[idx])
    plt.yticks(range(len(features)), np.array(features)[idx])
    plt.title("Process Bottleneck Importance")
    plt.tight_layout()
    plt.show()


def detect_bottlenecks(df, model, scaler, features):
    X = scaler.transform(df[features])
    preds = model.predict(X)

    df = df.copy()
    df["predicted_output"] = preds
    df["inefficiency_score"] = df["cost"] / (df["output"] + 1)

    bottlenecks = df.sort_values("inefficiency_score", ascending=False).head(10)

    print("\n=== TOP BOTTLENECKS ===")
    print(bottlenecks[features + ["cost", "output", "inefficiency_score"]])

    return df


def suggest_improvements(df):
    suggestions = []

    if df["wait_time"].mean() > 25:
        suggestions.append("Reduce waiting time via workflow automation.")

    if df["process_time"].mean() > 60:
        suggestions.append("Optimize process execution steps to reduce processing time.")

    if df["defect_rate"].mean() > 0.05:
        suggestions.append("Improve quality control to reduce defect rate.")

    if df["machine_utilization"].mean() < 0.6:
        suggestions.append("Increase machine utilization through better scheduling.")

    if df["material_cost"].mean() > 150:
        suggestions.append("Negotiate supplier contracts to reduce material costs.")

    print("\n=== PROCESS IMPROVEMENT SUGGESTIONS ===")
    for s in suggestions:
        print("-", s)


def visualize_data(df):
    plt.figure()
    plt.scatter(df["process_time"], df["output"], alpha=0.5)
    plt.title("Process Time vs Output")
    plt.xlabel("Process Time")
    plt.ylabel("Output")
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.scatter(df["wait_time"], df["output"], alpha=0.5)
    plt.title("Wait Time vs Output")
    plt.xlabel("Wait Time")
    plt.ylabel("Output")
    plt.tight_layout()
    plt.show()


def main():
    df = generate_operational_data()

    model, scaler, features = train_model(df)

    feature_importance(model, features)

    df = detect_bottlenecks(df, model, scaler, features)

    suggest_improvements(df)

    visualize_data(df)


if __name__ == "__main__":
    main()