"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# API Key for OpenWeatherMap
API_KEY = "YOUR_API_KEY"

# Function to fetch live weather data
def get_weather_data(city):
    try:
        # Construct API request URL
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        # Send GET request to API
        response = requests.get(url)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract relevant data
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        # Return weather data as a dictionary
        return {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed
        }
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions raised during the request
        print(f"Error fetching weather data: {e}")
        return None

# Function to update the weather dashboard
def update_weather_dashboard():
    # Get the city from the text entry field
    city = city_entry.get()
    
    # Fetch live weather data for the city
    weather_data = get_weather_data(city)
    
    # If weather data is available, update the dashboard
    if weather_data:
        # Update temperature label
        temperature_label.config(text=f"Temperature: {weather_data['temperature']}°C")
        
        # Update humidity label
        humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        
        # Update wind speed label
        wind_speed_label.config(text=f"Wind Speed: {weather_data['wind_speed']} m/s")
    
    # Schedule the next update
    root.after(60000, update_weather_dashboard)  # Update every 1 minute

# Create the main window
root = tk.Tk()
root.title("Live Weather Dashboard")

# Create a notebook to hold the dashboard and input field
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create a frame for the input field
input_frame = tk.Frame(notebook)
notebook.add(input_frame, text="Input")

# Create a label and entry field for the city
city_label = tk.Label(input_frame, text="City:")
city_label.pack()
city_entry = tk.Entry(input_frame)
city_entry.pack()

# Create a button to fetch and display weather data
fetch_button = tk.Button(input_frame, text="Fetch Weather", command=update_weather_dashboard)
fetch_button.pack()

# Create a frame for the weather dashboard
dashboard_frame = tk.Frame(notebook)
notebook.add(dashboard_frame, text="Dashboard")

# Create labels to display weather data
temperature_label = tk.Label(dashboard_frame, text="Temperature: ")
temperature_label.pack()
humidity_label = tk.Label(dashboard_frame, text="Humidity: ")
humidity_label.pack()
wind_speed_label = tk.Label(dashboard_frame, text="Wind Speed: ")
wind_speed_label.pack()

# Schedule the first update
update_weather_dashboard()

# Start the main loop
root.mainloop()