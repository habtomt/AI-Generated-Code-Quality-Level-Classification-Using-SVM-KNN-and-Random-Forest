"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_001.txt
Run      : 1
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def get_weather_data(api_key, location, start_date, end_date):
    # Example uses OpenWeatherMap API to get historical weather data
    # You will need an API key and check the API documentation for endpoint and parameters
    base_url = "http://api.weatherapi.com/v1/history.json"

    dates = pd.date_range(start=start_date, end=end_date)
    records = []

    for date in dates:
        params = {
            'key': api_key,
            'q': location,
            'dt': date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        except requests.RequestException as e:
            print(f"Failed to get data for date: {date.strftime('%Y-%m-%d')}")
            continue
        
        data = response.json()['forecast']['forecastday'][0]['day']
        records.append({
            'date': date,
            'avg_temp': data['avgtemp_c'],
            'precipitation': data['totalprecip_mm'],
            'max_temp': data['maxtemp_c'],
            'min_temp': data['mintemp_c'],
            # Add any additional necessary fields
        })
    
    return pd.DataFrame(records)

def analyze_weather_data(data):
    print(f"Average temperature: {data['avg_temp'].mean():.2f} °C")
    print(f"Total precipitation: {data['precipitation'].sum():.2f} mm")
    print(f"Minimum temperature: {data['min_temp'].min():.2f} °C")
    print(f"Maximum temperature: {data['max_temp'].max():.2f} °C")

def visualize_weather_data(data):
    sns.set_theme(style="darkgrid")

    # Plot Temperature trends
    plt.figure(figsize=(14, 7))
    plt.plot(data['date'], data['avg_temp'], label='Average Temperature (°C)')
    plt.plot(data['date'], data['max_temp'], label='Maximum Temperature (°C)')
    plt.plot(data['date'], data['min_temp'], label='Minimum Temperature (°C)')
    plt.title('Temperature Trend')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.xticks(rotation=45)

    # Plot Precipitation trends
    plt.figure(figsize=(14, 7))
    plt.plot(data['date'], data['precipitation'], label='Precipitation (mm)')
    plt.title('Precipitation Trend')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.legend()
    plt.xticks(rotation=45)

    plt.show()

def main():
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    location = 'London'
    start_date = '2023-09-01'
    end_date = '2023-09-30'

    weather_data = get_weather_data(api_key, location, start_date, end_date)
    analyze_weather_data(weather_data)
    visualize_weather_data(weather_data)

if __name__ == "__main__":
    main()