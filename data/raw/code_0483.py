"""
Auto-generated Python code
Scenario : Geolocation & Mapping
Prompt   : response_001.txt
Run      : 3
"""

import networkx as nx
import numpy as np
from math import radians, cos, sin, sqrt, atan2
import requests

# Set API key for traffic conditions (e.g. Google Maps API)
API_KEY = "YOUR_API_KEY"

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = earth_radius * c
    return distance

# Function to retrieve traffic conditions for a given location
def get_traffic_conditions(lat, lon):
    try:
        response = requests.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat},{lon}&destinations={lat},{lon}&mode=driving&traffic_model=pessimistic&key={API_KEY}")
        data = response.json()
        traffic_time = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
        return traffic_time
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving traffic conditions: {e}")
        return None

# Function to create a graph of delivery locations
def create_graph(delivery_locations):
    G = nx.Graph()
    for i in range(len(delivery_locations)):
        for j in range(i+1, len(delivery_locations)):
            lat1, lon1 = delivery_locations[i]
            lat2, lon2 = delivery_locations[j]
            distance = calculate_distance(lat1, lon1, lat2, lon2)
            traffic_time = get_traffic_conditions(lat1, lon1)  # Assume same traffic conditions for now
            if traffic_time:
                G.add_edge(i, j, weight=distance + traffic_time)
    return G

# Function to optimize delivery routes using the nearest neighbor algorithm
def optimize_routes(graph, num_vehicles, delivery_locations):
    num_deliveries = len(delivery_locations)
    routes = [[] for _ in range(num_vehicles)]
    for i in range(num_deliveries):
        # Find the closest unserved location
        closest_location = None
        min_distance = float('inf')
        for j in range(num_vehicles):
            if not routes[j]:
                continue
            for k in range(len(routes[j])):
                edge = routes[j][k-1]
                distance = graph.get_edge_data(edge[0], edge[1])['weight']
                if distance < min_distance:
                    min_distance = distance
                    closest_location = (j, k)
        # Assign the current delivery to the closest route
        routes[closest_location[0]].append(i)
    return routes

# Example usage:
delivery_locations = [(40.7128, -74.0060), (34.0522, -118.2437), (41.8781, -87.6298), (29.7604, -95.3698)]
num_vehicles = 2
graph = create_graph(delivery_locations)
routes = optimize_routes(graph, num_vehicles, delivery_locations)

for i, route in enumerate(routes):
    print(f"Vehicle {i+1}:")
    for delivery in route:
        print(f"  Delivery {delivery}: {delivery_locations[delivery]}")
    print()