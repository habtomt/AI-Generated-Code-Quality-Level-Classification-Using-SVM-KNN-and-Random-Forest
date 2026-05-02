"""
Auto-generated Python code
Scenario : Geolocation & Mapping
Prompt   : response_003.txt
Run      : 2
"""

# Import required libraries
import pandas as pd
import geopy.distance
from geopy.geocoders import Nominatim
import requests
import gpx
from datetime import datetime

# Set up API key for OpenWeatherMap (replace with your own key)
OPENWEATHERMAP_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

# Define a class to record physical activities
class PhysicalActivity:
    def __init__(self, user_id, activity_type):
        """
        Initialize a physical activity record.

        Args:
            user_id (str): The ID of the user.
            activity_type (str): The type of physical activity (e.g., running, cycling).
        """
        self.user_id = user_id
        self.activity_type = activity_type
        self.route_points = []
        self.distance = 0
        self.speed = 0
        self.start_time = None
        self.end_time = None

    def add_route_point(self, latitude, longitude, elevation):
        """
        Add a route point to the activity record.

        Args:
            latitude (float): The latitude of the route point.
            longitude (float): The longitude of the route point.
            elevation (float): The elevation of the route point.
        """
        self.route_points.append((latitude, longitude, elevation))

    def calculate_distance(self):
        """
        Calculate the total distance of the route.
        """
        if self.route_points:
            self.distance = sum(
                geopy.distance.geodesic(point1, point2).meters
                for i, point1 in enumerate(self.route_points)
                for point2 in self.route_points[i + 1:]
            ) / 1609.34  # Convert meters to miles

    def calculate_speed(self):
        """
        Calculate the average speed of the route.
        """
        if self.route_points:
            self.speed = self.distance / (self.end_time - self.start_time).total_seconds() / 60  # Convert seconds to minutes

    def get_weather_data(self, latitude, longitude):
        """
        Get the weather data for the route.

        Args:
            latitude (float): The latitude of the route point.
            longitude (float): The longitude of the route point.

        Returns:
            dict: The weather data.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHERMAP_API_KEY}"
        response = requests.get(url)
        return response.json()

    def save_to_gpx(self, filename):
        """
        Save the route to a GPX file.

        Args:
            filename (str): The filename of the GPX file.
        """
        gpx_file = gpx.GPX()
        gpx_track = gpx_file.creator("Physical Activity Tracker")
        gpx_segment = gpx_track.new_segment()
        for point in self.route_points:
            gpx_segment.new_point(point[0], point[1], point[2])
        gpx_file.write(filename, pretty=True)

# Create a new physical activity record
activity = PhysicalActivity("USER123", "running")

# Add route points to the activity record
activity.add_route_point(37.7749, -122.4194, 10)
activity.add_route_point(37.7858, -122.4364, 20)
activity.add_route_point(37.7963, -122.4574, 15)

# Calculate the distance of the route
activity.calculate_distance()

# Calculate the speed of the route
activity.start_time = datetime(2023, 3, 1, 10, 0, 0)
activity.end_time = datetime(2023, 3, 1, 11, 30, 0)
activity.calculate_speed()

# Get the weather data for the route
weather_data = activity.get_weather_data(37.7749, -122.4194)

# Save the route to a GPX file
activity.save_to_gpx("physical_activity.gpx")

# Print the activity metrics
print(f"User ID: {activity.user_id}")
print(f"Activity Type: {activity.activity_type}")
print(f"Distance: {activity.distance} miles")
print(f"Speed: {activity.speed} mph")
print("Weather Data:")
print(weather_data)