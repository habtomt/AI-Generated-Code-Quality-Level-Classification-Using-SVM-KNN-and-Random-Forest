#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_synthetic_traffic(n_samples=5000):
    np.random.seed(42)

    timestamps = pd.date_range(start="2025-01-01", periods=n_samples, freq="H")

    hours = timestamps.hour

    base_traffic = (
        np.sin((hours / 24) * 2 * np.pi) * 50
        + np.random.normal(100, 20, n_samples)
    )

    age = np.random.choice(
        [18, 25, 35, 45, 55, 65],
        size=n_samples,
        p=[0.2, 0.25, 0.2, 0.15, 0.1, 0.1],
    )

    engagement_time = np.abs(np.random.normal(3, 1.5, n_samples))

    pages_viewed = np.random.poisson(5, n_samples)

    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Hour": hours,
        "Traffic": base_traffic,
        "Age": age,
        "EngagementTime": engagement_time,
        "PagesViewed": pages_viewed
    })

    return df


def analyze_peak_hours(df):
    hourly = df.groupby("Hour")["Traffic"].mean()

    plt.figure()
    plt.plot(hourly.index, hourly.values)
    plt.title("Average Traffic by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Traffic")
    plt.show()


def analyze_demographics(df):
    demo = df.groupby("Age")["EngagementTime"].mean()

    plt.figure()
    plt.bar(demo.index.astype(str), demo.values)
    plt.title("Engagement Time by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Engagement Time (min)")
    plt.show()


def engagement_analysis(df):
    plt.figure()
    plt.scatter(df["PagesViewed"], df["EngagementTime"], alpha=0.4)
    plt.title("Pages Viewed vs Engagement Time")
    plt.xlabel("Pages Viewed")
    plt.ylabel("Engagement Time")
    plt.show()


def traffic_trend(df):
    daily = df.set_index("Timestamp").resample("D")["Traffic"].mean()

    plt.figure()
    plt.plot(daily.index, daily.values)
    plt.title("Daily Website Traffic Trend")
    plt.xlabel("Date")
    plt.ylabel("Traffic")
    plt.show()


def main():
    df = generate_synthetic_traffic()

    analyze_peak_hours(df)
    analyze_demographics(df)
    engagement_analysis(df)
    traffic_trend(df)

    print(df.describe())


if __name__ == "__main__":
    main()