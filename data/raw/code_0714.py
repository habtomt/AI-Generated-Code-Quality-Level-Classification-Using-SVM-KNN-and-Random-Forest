"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from datetime import datetime, timedelta

# Replace with your own API key
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city, start_date, end_date):
    try:
        # Set API request parameters
        params = {
            "q": city,
            "units": "metric",
            "appid": API_KEY
        }

        # Loop through each day in the specified period
        weather_data = []
        current_date = start_date
        while current_date <= end_date:
            # Make API request for current date
            response = requests.get(f"http://api.openweathermap.org/data/2.5/onecall/timemachine", params=params)
            response.raise_for_status()
            data = response.json()

            # Extract relevant weather data
            date = current_date.strftime("%Y-%m-%d")
            temp = data["current"]["temp"]
            feels_like = data["current"]["feels_like"]
            precipitation = data["daily"][0]["rain"]["1h"] if "rain" in data["daily"][0] else 0

            # Append data to list
            weather_data.append({
                "Date": date,
                "Temperature (°C)": temp,
                "Feels Like (°C)": feels_like,
                "Precipitation (mm)": precipitation
            })

            # Increment date by one day
            current_date += timedelta(days=1)

        # Convert list to Pandas DataFrame
        df = pd.DataFrame(weather_data)

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Function to visualize weather data
def visualize_weather_data(df):
    try:
        # Plot temperature and feels like temperature over time
        plt.figure(figsize=(10,6))
        plt.plot(df["Date"], df["Temperature (°C)"], label="Temperature")
        plt.plot(df["Date"], df["Feels Like (°C)"], label="Feels Like Temperature")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.title("Temperature and Feels Like Temperature Over Time")
        plt.legend()
        plt.show()

        # Plot precipitation over time
        plt.figure(figsize=(10,6))
        plt.bar(df["Date"], df["Precipitation (mm)"])
        plt.xlabel("Date")
        plt.ylabel("Precipitation (mm)")
        plt.title("Precipitation Over Time")
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

# Main program
def main():
    city = "London"  # Replace with your own city
    start_date = datetime(2024, 1, 1)  # Start date (YYYY-MM-DD)
    end_date = datetime(2024, 1, 31)  # End date (YYYY-MM-DD)

    # Get weather data for specified period
    df = get_weather_data(city, start_date, end_date)

    # Visualize weather data
    if df is not None:
        visualize_weather_data(df)

if __name__ == "__main__":
    main()