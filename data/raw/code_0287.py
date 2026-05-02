import requests
from datetime import datetime

# Configuration
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_forecast(city):
    """Fetches a 5-day / 3-hour forecast for the given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def find_optimal_times(forecast_data, preferred_temp=(15, 25), max_wind=5, avoid_rain=True):
    """
    Analyzes forecast data to suggest optimal event slots.
    Default 'Optimal' = 15-25°C, Low wind, No rain.
    """
    suggestions = []
    
    for entry in forecast_data['list']:
        dt = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        wind = entry['wind']['speed']
        weather_main = entry['weather'][0]['main']
        description = entry['weather'][0]['description']
        
        # Scoring logic
        is_good_temp = preferred_temp[0] <= temp <= preferred_temp[1]
        is_low_wind = wind <= max_wind
        is_dry = weather_main != "Rain" if avoid_rain else True
        
        if is_good_temp and is_low_wind and is_dry:
            suggestions.append({
                "time": dt.strftime("%Y-%m-%d %H:%M"),
                "temp": temp,
                "wind": wind,
                "desc": description
            })
            
    return suggestions

def main():
    print("--- Weather-Based Event Scheduler ---")
    city = input("Enter city name: ").strip()
    
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        print("Please update the script with your OpenWeatherMap API Key.")
        return

    data = get_forecast(city)
    
    if data:
        print(f"\nAnalyzing next 5 days for {city}...")
        optimal_slots = find_optimal_times(data)
        
        if optimal_slots:
            print("\nRecommended Times for your Event:")
            print(f"{'Date & Time':<20} | {'Temp':<7} | {'Wind':<7} | {'Condition'}")
            print("-" * 55)
            for slot in optimal_slots[:10]:  # Show top 10 suggestions
                print(f"{slot['time']:<20} | {slot['temp']:>4}°C | {slot['wind']:>3}m/s | {slot['desc']}")
        else:
            print("\nNo optimal windows found matching your criteria in the next 5 days.")

if __name__ == "__main__":
    main()