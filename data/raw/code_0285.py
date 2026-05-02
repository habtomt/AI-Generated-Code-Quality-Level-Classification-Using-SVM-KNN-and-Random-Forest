import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime

class WeatherAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"
        sns.set_theme(style="darkgrid")

    def fetch_data(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def process_data(self, raw_data):
        records = []
        for entry in raw_data['list']:
            records.append({
                "datetime": datetime.fromtimestamp(entry['dt']),
                "temp": entry['main']['temp'],
                "humidity": entry['main']['humidity'],
                "precipitation": entry.get('rain', {}).get('3h', 0),
                "wind_speed": entry['wind']['speed']
            })
        return pd.DataFrame(records)

    def visualize_trends(self, df, city_name):
        fig, axes = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
        fig.suptitle(f"Weather Trends Analysis: {city_name}", fontsize=16)

        # Temperature Trend
        sns.lineplot(ax=axes[0], data=df, x="datetime", y="temp", color="orange", marker="o")
        axes[0].set_title("Temperature Variations (°C)")
        axes[0].set_ylabel("Temp (°C)")

        # Precipitation Pattern
        sns.barplot(ax=axes[1], data=df, x="datetime", y="precipitation", color="skyblue")
        axes[1].set_title("Precipitation Levels (mm)")
        axes[1].set_ylabel("Rain (3h)")

        # Humidity and Wind
        sns.lineplot(ax=axes[2], data=df, x="datetime", y="humidity", color="green", label="Humidity %")
        ax2 = axes[2].twinx()
        sns.lineplot(ax=ax2, data=df, x="datetime", y="wind_speed", color="purple", label="Wind Speed")
        axes[2].set_title("Humidity vs Wind Speed")
        axes[2].set_ylabel("Humidity (%)")
        ax2.set_ylabel("Wind (m/s)")

        plt.xticks(rotation=45)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

def main():
    # Replace with a valid OpenWeatherMap API Key
    API_KEY = "YOUR_API_KEY_HERE"
    CITY = "London"

    analyzer = WeatherAnalyzer(API_KEY)
    
    try:
        print(f"Retrieving data for {CITY}...")
        raw_json = analyzer.fetch_data(CITY)
        df = analyzer.process_data(raw_json)
        
        print("Analyzing trends...")
        print(df.describe())
        
        analyzer.visualize_trends(df, CITY)
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()