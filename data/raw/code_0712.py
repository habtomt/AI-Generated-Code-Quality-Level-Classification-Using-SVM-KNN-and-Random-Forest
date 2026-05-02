"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
import requests
import json
import datetime
from datetime import timedelta
import tkinter as tk
from tkinter import ttk

# Set up API keys and endpoints
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
OPENWEATHERMAP_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast"
CROP_TYPES = {
    "wheat": {"optimal_temperature": 18, "optimal_humidity": 60},
    "maize": {"optimal_temperature": 20, "optimal_humidity": 70},
    "soybeans": {"optimal_temperature": 22, "optimal_humidity": 80}
}

class FarmerAdvisoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Farmer Advisory App")
        self.root.geometry("800x600")

        # Create main frames
        self.top_frame = tk.Frame(self.root)
        self.bottom_frame = tk.Frame(self.root)

        # Create input fields
        self.location_label = tk.Label(self.top_frame, text="Location (City, Country):")
        self.location_label.pack(side=tk.LEFT)
        self.location_entry = tk.Entry(self.top_frame, width=50)
        self.location_entry.pack(side=tk.LEFT)

        self.crop_type_label = tk.Label(self.top_frame, text="Crop Type (wheat, maize, soybeans):")
        self.crop_type_label.pack(side=tk.LEFT)
        self.crop_type_entry = tk.Entry(self.top_frame, width=20)
        self.crop_type_entry.pack(side=tk.LEFT)

        # Create buttons
        self.get_weather_button = tk.Button(self.top_frame, text="Get Weather Forecast", command=self.get_weather_forecast)
        self.get_weather_button.pack(side=tk.LEFT)

        # Create output fields
        self.weather_forecast_label = tk.Label(self.bottom_frame, text="Weather Forecast:")
        self.weather_forecast_label.pack(side=tk.LEFT)

        self.recommendations_label = tk.Label(self.bottom_frame, text="Recommendations:")
        self.recommendations_label.pack(side=tk.LEFT)

        # Pack frames
        self.top_frame.pack()
        self.bottom_frame.pack()

    def get_weather_forecast(self):
        # Get location and crop type from input fields
        location = self.location_entry.get()
        crop_type = self.crop_type_entry.get()

        # Validate input
        if not location or not crop_type:
            self.weather_forecast_label.config(text="Please enter location and crop type")
            return

        # Call OpenWeatherMap API to get weather forecast
        try:
            params = {
                "q": location,
                "appid": API_KEY,
                "units": "metric"
            }
            response = requests.get(OPENWEATHERMAP_ENDPOINT, params=params)
            weather_data = response.json()

            # Process weather data
            self.process_weather_data(weather_data, crop_type)
        except requests.exceptions.RequestException as e:
            self.weather_forecast_label.config(text="Error getting weather forecast: " + str(e))

    def process_weather_data(self, weather_data, crop_type):
        # Get current date and time
        current_date = datetime.datetime.now()

        # Initialize recommendations
        recommendations = []

        # Loop through weather data and find optimal planting, harvesting, and protection times
        for forecast in weather_data["list"]:
            date = datetime.datetime.fromtimestamp(forecast["dt"])
            temperature = forecast["main"]["temp"]
            humidity = forecast["main"]["humidity"]

            # Check if current date matches the date of the forecast
            if date.date() == current_date.date():
                # Check if temperature and humidity are within optimal ranges for the crop
                if (crop_type == "wheat" and temperature >= CROP_TYPES[crop_type]["optimal_temperature"] and humidity >= CROP_TYPES[crop_type]["optimal_humidity"]) or \
                   (crop_type == "maize" and temperature >= CROP_TYPES[crop_type]["optimal_temperature"] and humidity >= CROP_TYPES[crop_type]["optimal_humidity"]) or \
                   (crop_type == "soybeans" and temperature >= CROP_TYPES[crop_type]["optimal_temperature"] and humidity >= CROP_TYPES[crop_type]["optimal_humidity"]):
                    # Add recommendation to list
                    recommendations.append(f"Plant {crop_type} on {date.strftime('%Y-%m-%d')}")

        # Display weather forecast and recommendations
        self.weather_forecast_label.config(text="Weather Forecast:")
        for forecast in weather_data["list"]:
            date = datetime.datetime.fromtimestamp(forecast["dt"])
            self.weather_forecast_label.config(text=self.weather_forecast_label.cget("text") + f"\n{date.strftime('%Y-%m-%d')}: {forecast['weather'][0]['description']}")

        self.recommendations_label.config(text="Recommendations:")
        for recommendation in recommendations:
            self.recommendations_label.config(text=self.recommendations_label.cget("text") + f"\n{recommendation}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FarmerAdvisoryApp(root)
    root.mainloop()