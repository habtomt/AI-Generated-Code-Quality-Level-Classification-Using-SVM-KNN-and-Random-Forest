import requests
import sys

def get_weather(city, api_key):
    """
    Fetches live weather data from OpenWeatherMap API.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": "City not found or API key invalid."}
    except Exception as e:
        return {"error": str(e)}

def display_dashboard(data):
    """
    Renders a simple CLI dashboard.
    """
    if "error" in data:
        print(f"\n[!] Error: {data['error']}")
        return

    name = data.get("name")
    country = data.get("sys", {}).get("country")
    temp = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    wind_speed = data.get("wind", {}).get("speed")
    desc = data.get("weather", [{}])[0].get("description", "N/A").capitalize()

    print("\n" + "="*40)
    print(f" LIVE WEATHER DASHBOARD: {name}, {country} ")
    print("="*40)
    print(f" Status:      {desc}")
    print(f" Temperature: {temp}°C")
    print(f" Humidity:    {humidity}%")
    print(f" Wind Speed:  {wind_speed} m/s")
    print("="*40 + "\n")

def main():
    # Replace 'YOUR_API_KEY' with a valid OpenWeatherMap API key
    API_KEY = "YOUR_API_KEY"
    
    print("Weather Data Fetcher")
    while True:
        city = input("Enter city name (or 'exit' to quit): ").strip()
        if city.lower() == 'exit':
            break
        
        if API_KEY == "YOUR_API_KEY":
            print("\n[!] Please provide a valid OpenWeatherMap API key in the source code.")
            break

        weather_data = get_weather(city, API_KEY)
        display_dashboard(weather_data)

if __name__ == "__main__":
    main()