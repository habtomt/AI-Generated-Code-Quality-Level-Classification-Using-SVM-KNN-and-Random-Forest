"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_003.txt
Run      : 2
"""

import requests
import datetime
import pytz
from dateutil import tz
from datetime import timedelta

# Replace with your OpenWeatherMap API key
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

def get_weather_forecast(location, api_key):
    """
    Get the weather forecast for a given location.
    
    Args:
        location (str): City name or zip code.
        api_key (str): OpenWeatherMap API key.
    
    Returns:
        dict: Weather forecast data.
    """
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def suggest_optimal_time(weather_forecast):
    """
    Suggest optimal time for scheduling events based on weather conditions.
    
    Args:
        weather_forecast (dict): Weather forecast data.
    
    Returns:
        tuple: Suggested time (hour) and weather condition.
    """
    # Find the time with the least precipitation
    optimal_time = None
    min_precipitation = float('inf')
    
    for forecast in weather_forecast["list"]:
        precipitation = forecast["rain"]["3h"] if "rain" in forecast else 0
        if precipitation < min_precipitation:
            min_precipitation = precipitation
            optimal_time = forecast["dt_txt"]
    
    # Convert the suggested time to 12-hour format
    suggested_time = pytz.timezone('US/Eastern').localize(datetime.datetime.strptime(optimal_time, "%Y-%m-%d %H:%M:%S")).astimezone(tz.tzlocal()).strftime("%I:%M %p")
    weather_condition = "Sunny" if min_precipitation == 0 else "Partly Cloudy"
    
    return suggested_time, weather_condition

def main():
    # Replace with your location
    location = "New York"
    
    # Get the weather forecast
    weather_forecast = get_weather_forecast(location, API_KEY)
    
    # Suggest the optimal time for scheduling events
    if weather_forecast:
        suggested_time, weather_condition = suggest_optimal_time(weather_forecast)
        print(f"Optimal time to schedule events: {suggested_time} ({weather_condition})")
    else:
        print("Failed to retrieve weather forecast.")

if __name__ == "__main__":
    main()