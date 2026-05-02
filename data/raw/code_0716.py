"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_003.txt
Run      : 3
"""

# Required imports
import requests
import datetime
import pytz
from datetime import timedelta

# Set your API key for OpenWeatherMap
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

def get_weather_forecast(city, api_key):
    """
    Retrieves the weather forecast for a given city.
    
    Args:
    city (str): The city for which to retrieve the forecast.
    api_key (str): Your OpenWeatherMap API key.
    
    Returns:
    dict: The weather forecast data.
    """
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving weather forecast: {e}")
        return None

def suggest_optimal_times(forecast_data):
    """
    Suggests optimal times for scheduling events based on the weather forecast.
    
    Args:
    forecast_data (dict): The weather forecast data.
    
    Returns:
    list: A list of tuples containing the optimal time and a brief description.
    """
    optimal_times = []
    for i in range(0, len(forecast_data['list']), 8):  # Check every 8th entry (1 hour intervals)
        entry = forecast_data['list'][i]
        time = datetime.datetime.fromtimestamp(entry['dt'], pytz.UTC)
        description = entry['weather'][0]['description']
        if "clear sky" in description.lower() or "light rain" in description.lower():  # Suggest times for clear or light rain conditions
            optimal_times.append((time, "Good time for outdoor events"))
        elif "sunny" in description.lower():  # Suggest times for sunny conditions
            optimal_times.append((time, "Good time for outdoor events"))
        elif "light snow" in description.lower() or "heavy snow" in description.lower():  # Suggest times for snowy conditions
            optimal_times.append((time, "Good time for winter sports"))
    return optimal_times

def main():
    city = input("Enter the city for which to retrieve the weather forecast: ")
    forecast_data = get_weather_forecast(city, API_KEY)
    if forecast_data:
        optimal_times = suggest_optimal_times(forecast_data)
        if optimal_times:
            print("Optimal times for scheduling events:")
            for time, description in optimal_times:
                print(f"{time.strftime('%Y-%m-%d %H:%M')} - {description}")
        else:
            print("No optimal times found.")
    else:
        print("Failed to retrieve weather forecast.")

if __name__ == "__main__":
    main()