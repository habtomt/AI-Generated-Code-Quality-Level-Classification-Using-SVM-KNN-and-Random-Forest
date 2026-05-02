"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_000.txt
Run      : 2
"""

# Import required libraries
import requests
import tkinter as tk
from tkinter import ttk
import time

# Your OpenWeatherMap API key
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Weather Dashboard")
        self.root.geometry("300x200")

        # Create a frame for the dashboard
        self.dashboard = ttk.Frame(self.root)
        self.dashboard.pack(fill="both", expand=True)

        # Create labels for weather data
        self.temperature_label = ttk.Label(self.dashboard, text="Temperature: ")
        self.temperature_label.pack()

        self.humidity_label = ttk.Label(self.dashboard, text="Humidity: ")
        self.humidity_label.pack()

        self.wind_speed_label = ttk.Label(self.dashboard, text="Wind Speed: ")
        self.wind_speed_label.pack()

        # Create a button to refresh the weather data
        self.refresh_button = ttk.Button(self.dashboard, text="Refresh", command=self.refresh_weather)
        self.refresh_button.pack()

        # Fetch and display initial weather data
        self.refresh_weather()

    def refresh_weather(self):
        try:
            # Make a GET request to the OpenWeatherMap API
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&units=metric")

            # Check if the response was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Extract temperature, humidity, and wind speed from the JSON response
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                # Update the labels with the weather data
                self.temperature_label.config(text=f"Temperature: {temperature}°C")
                self.humidity_label.config(text=f"Humidity: {humidity}%")
                self.wind_speed_label.config(text=f"Wind Speed: {wind_speed} m/s")

            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

# Create the main window
root = tk.Tk()

# Create an instance of the WeatherDashboard class
weather_dashboard = WeatherDashboard(root)

# Start the main loop
root.mainloop()