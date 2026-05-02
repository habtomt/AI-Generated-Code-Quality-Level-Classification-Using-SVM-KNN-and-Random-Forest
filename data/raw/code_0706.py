"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_003.txt
Run      : 1
"""

import requests
from datetime import datetime, timedelta
import pytz
from tzlocal import get_localzone

API_KEY = 'YOUR_API_KEY'
CITY_ID = '2950159'  # New York City

def get_weather_data(api_key, city_id):
    url = f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error fetching weather data: {err}")
        return None
    data = response.json()
    return data

def process_weather_data(weather_data):
    # This function processes the weather data to find optimal times.
    # For simplicity, let's assume optimal times are those with no rain and moderate temperature.
    optimal_times = []

    for entry in weather_data['list']:
        dt = entry['dt_txt']
        dt_obj = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        dt_local = get_localzone().localize(dt_obj)
        weather_description = entry['weather'][0]['description']
        temp = entry['main']['temp'] - 273.15  # Convert Kelvin to Celsius

        if 'rain' not in weather_description.lower() and 15 <= temp <= 25:
            optimal_times.append(dt_local)

    return optimal_times

def main():
    print("Event Scheduling Tool with Weather Forecast")

    weather_data = get_weather_data(API_KEY, CITY_ID)
    
    if weather_data:
        optimal_times = process_weather_data(weather_data)

        if optimal_times:
            print("Optimal times for your event based on weather forecast:")
            for opt_time in optimal_times:
                print(f"- {opt_time.strftime('%Y-%m-%d %H:%M:%S')} ({opt_time.tzname()})")
        else:
            print("No optimal times found based on the current forecast.")
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    main()