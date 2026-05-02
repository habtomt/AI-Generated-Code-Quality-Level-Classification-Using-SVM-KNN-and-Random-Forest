"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_001.txt
Run      : 2
"""

# Required libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import datetime

# API Endpoint and Key
api_key = "YOUR_OPENWEATHERMAP_API_KEY"
base_url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=37.794&lon=-122.406&dt={datetime.date.today().timestamp() - 86400}&appid={api_key}"

# Function to get weather data
def get_weather_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to extract relevant data
def extract_data(weather_data):
    try:
        data = pd.DataFrame(weather_data['hourly'])
        data.dropna(inplace=True)
        return data[['temp', 'humidity', 'wind_speed', 'weather.description']]
    except KeyError as e:
        print(f"Error extracting data: {e}")
        return None

# Function to visualize data
def visualize_data(data):
    try:
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        
        # Temperature
        axs[0, 0].plot(data['temp'])
        axs[0, 0].set_title('Temperature Trend')
        axs[0, 0].set_xlabel('Hour')
        axs[0, 0].set_ylabel('Temperature (K)')
        
        # Humidity
        axs[0, 1].plot(data['humidity'])
        axs[0, 1].set_title('Humidity Trend')
        axs[0, 1].set_xlabel('Hour')
        axs[0, 1].set_ylabel('Humidity (%)')
        
        # Wind Speed
        axs[1, 0].plot(data['wind_speed'])
        axs[1, 0].set_title('Wind Speed Trend')
        axs[1, 0].set_xlabel('Hour')
        axs[1, 0].set_ylabel('Wind Speed (m/s)')
        
        # Weather Description
        axs[1, 1].plot(data['weather.description'])
        axs[1, 1].set_title('Weather Description Trend')
        axs[1, 1].set_xlabel('Hour')
        axs[1, 1].set_ylabel('Description')
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error visualizing data: {e}")

# Main function
def main():
    url = base_url
    weather_data = get_weather_data(url)
    data = extract_data(weather_data)
    visualize_data(data)

# Run the main function
if __name__ == "__main__":
    main()