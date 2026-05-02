# weather_analysis.py

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def fetch_weather_data(latitude, longitude, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max"
        ],
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    daily = data["daily"]

    df = pd.DataFrame({
        "date": daily["time"],
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "precipitation": daily["precipitation_sum"],
        "wind_speed": daily["windspeed_10m_max"]
    })

    df["date"] = pd.to_datetime(df["date"])
    return df


def plot_weather(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["temp_max"], label="Max Temp (°C)")
    plt.plot(df["date"], df["temp_min"], label="Min Temp (°C)")
    plt.title("Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.bar(df["date"], df["precipitation"], label="Precipitation (mm)")
    plt.title("Precipitation Trend")
    plt.xlabel("Date")
    plt.ylabel("Precipitation (mm)")
    plt.grid()
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["wind_speed"], label="Wind Speed (km/h)", color="green")
    plt.title("Wind Speed Trend")
    plt.xlabel("Date")
    plt.ylabel("Wind Speed (km/h)")
    plt.legend()
    plt.grid()
    plt.show()


def main():
    print("Weather Data Analyzer")

    latitude = float(input("Enter latitude (default Istanbul: 41.0082): ") or 41.0082)
    longitude = float(input("Enter longitude (default Istanbul: 28.9784): ") or 28.9784)

    days = int(input("Enter number of past days to analyze (max 30): ") or 7)

    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    print(f"Fetching data from {start_str} to {end_str}...")

    df = fetch_weather_data(latitude, longitude, start_str, end_str)

    print(df)

    plot_weather(df)


if __name__ == "__main__":
    main()