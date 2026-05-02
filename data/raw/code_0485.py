"""
Auto-generated Python code
Scenario : Geolocation & Mapping
Prompt   : response_003.txt
Run      : 3
"""

# Import necessary libraries
import datetime
import math
import pandas as pd
import numpy as np

# Define a class for physical activity
class PhysicalActivity:
    def __init__(self, user_id, activity_type):
        self.user_id = user_id
        self.activity_type = activity_type
        self.route = []
        self.metrics = {'distance': 0, 'speed': 0, 'calories_burned': 0}

    # Function to record location
    def record_location(self, latitude, longitude):
        self.route.append({'latitude': latitude, 'longitude': longitude})

    # Function to calculate distance between two points
    def calculate_distance(self, point1, point2):
        # Convert coordinates to radians
        lat1, lon1 = math.radians(point1['latitude']), math.radians(point1['longitude'])
        lat2, lon2 = math.radians(point2['latitude']), math.radians(point2['longitude'])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = 6371 * c  # Radius of the Earth in kilometers
        
        return distance

    # Function to calculate speed
    def calculate_speed(self):
        if len(self.route) > 1:
            previous_point = self.route[-2]
            current_point = self.route[-1]
            distance = self.calculate_distance(previous_point, current_point)
            time_diff = (datetime.datetime.now() - datetime.datetime.fromtimestamp(self.route[-2]['timestamp'])).total_seconds() / 3600  # Convert to hours
            self.metrics['speed'] = distance / time_diff
        else:
            self.metrics['speed'] = 0

    # Function to calculate calories burned
    def calculate_calories_burned(self):
        # Approximate calorie burn rate for running and cycling (from various sources)
        if self.activity_type == 'running':
            calories_per_km = 62.5
        elif self.activity_type == 'cycling':
            calories_per_km = 48.5
        else:
            calories_per_km = 0

        if len(self.route) > 1:
            total_distance = 0
            for i in range(1, len(self.route)):
                previous_point = self.route[i-1]
                current_point = self.route[i]
                distance = self.calculate_distance(previous_point, current_point)
                total_distance += distance

            self.metrics['calories_burned'] = total_distance * calories_per_km
        else:
            self.metrics['calories_burned'] = 0

# Define a class for the application
class Application:
    def __init__(self):
        self.users = {}

    # Function to add user
    def add_user(self, user_id, activity_type):
        if user_id not in self.users:
            self.users[user_id] = PhysicalActivity(user_id, activity_type)

    # Function to record location for a user
    def record_location(self, user_id, latitude, longitude):
        if user_id in self.users:
            self.users[user_id].record_location(latitude, longitude)
        else:
            print("User not found.")

    # Function to calculate metrics for a user
    def calculate_metrics(self, user_id):
        if user_id in self.users:
            self.users[user_id].calculate_distance()
            self.users[user_id].calculate_speed()
            self.users[user_id].calculate_calories_burned()
            return self.users[user_id].metrics
        else:
            print("User not found.")

# Create an instance of the application
app = Application()

# Add users
app.add_user('user1', 'running')
app.add_user('user2', 'cycling')

# Record locations
app.record_location('user1', 37.7749, -122.4194)
app.record_location('user1', 37.7859, -122.4364)
app.record_location('user2', 38.8977, -77.0365)
app.record_location('user2', 38.9061, -77.0521)

# Calculate metrics
print(app.calculate_metrics('user1'))
print(app.calculate_metrics('user2'))