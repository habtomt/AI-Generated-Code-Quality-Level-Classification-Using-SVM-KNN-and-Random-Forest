"""
Auto-generated Python code
Scenario : Geolocation & Mapping
Prompt   : response_001.txt
Run      : 2
"""

import math
from itertools import permutations
import requests

# Set API key for Google Maps API (free tier)
GOOGLE_MAPS_API_KEY = "YOUR_API_KEY"

# Define a class to represent a delivery location
class DeliveryLocation:
    def __init__(self, id, latitude, longitude, priority):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.priority = priority

# Define a function to calculate the distance between two points using Google Maps API
def calculate_distance(start, end):
    try:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={start.latitude},{start.longitude}&destinations={end.latitude},{end.longitude}&mode=driving&key={GOOGLE_MAPS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        distance = data["rows"][0]["elements"][0]["distance"]["value"] / 1000
        return distance
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return None

# Define a function to calculate the travel time between two points using Google Maps API
def calculate_travel_time(start, end):
    try:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={start.latitude},{start.longitude}&destinations={end.latitude},{end.longitude}&mode=driving&key={GOOGLE_MAPS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        travel_time = data["rows"][0]["elements"][0]["duration"]["value"] / 60
        return travel_time
    except Exception as e:
        print(f"Error calculating travel time: {e}")
        return None

# Define a function to calculate the total travel time and distance for a route
def calculate_route_metrics(route):
    total_distance = 0
    total_travel_time = 0
    for i in range(len(route) - 1):
        start = route[i]
        end = route[i + 1]
        distance = calculate_distance(start, end)
        if distance is not None:
            total_distance += distance
            travel_time = calculate_travel_time(start, end)
            if travel_time is not None:
                total_travel_time += travel_time
    return total_distance, total_travel_time

# Define a function to optimize the delivery route using the nearest neighbor algorithm
def optimize_route(delivery_locations):
    # Start at the first delivery location
    route = [delivery_locations[0]]
    visited = [delivery_locations[0].id]
    remaining_locations = delivery_locations[1:]

    while remaining_locations:
        closest_location = None
        closest_distance = float("inf")

        for location in remaining_locations:
            distance = calculate_distance(route[-1], location)
            if distance is not None and distance < closest_distance:
                closest_location = location
                closest_distance = distance

        if closest_location is not None:
            route.append(closest_location)
            visited.append(closest_location.id)
            remaining_locations.remove(closest_location)

    return route

# Define a function to print the optimized route
def print_route(route):
    print("Optimized Route:")
    for i, location in enumerate(route):
        print(f"  Delivery {i+1}: {location.id} ({location.latitude}, {location.longitude}) - Priority: {location.priority}")

# Create a list of delivery locations
delivery_locations = [
    DeliveryLocation(1, 37.7749, -122.4194, 3),
    DeliveryLocation(2, 37.7859, -122.4364, 1),
    DeliveryLocation(3, 37.7963, -122.4574, 2),
    DeliveryLocation(4, 37.8067, -122.4784, 4),
    DeliveryLocation(5, 37.8171, -122.4994, 5)
]

# Optimize the delivery route
optimized_route = optimize_route(delivery_locations)

# Calculate the total travel time and distance for the optimized route
total_distance, total_travel_time = calculate_route_metrics(optimized_route)

# Print the optimized route
print_route(optimized_route)

# Print the total travel time and distance
print(f"Total Travel Time: {total_travel_time} hours")
print(f"Total Distance: {total_distance} km")