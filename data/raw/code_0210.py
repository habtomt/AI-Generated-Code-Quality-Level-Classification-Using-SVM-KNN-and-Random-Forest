import time
import math
from datetime import datetime

class ActivityTracker:
    def __init__(self):
        self.route_points = []  # List of (lat, lon, timestamp)
        self.is_tracking = False

    def haversine_distance(self, coord1, coord2):
        """
        Calculates the great-circle distance between two points in kilometers.
        """
        R = 6371.0  # Earth radius in km
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def record_waypoint(self, lat, lon):
        """
        Simulates capturing a GPS ping.
        """
        timestamp = datetime.now()
        self.route_points.append((lat, lon, timestamp))

    def calculate_metrics(self):
        if len(self.route_points) < 2:
            return 0.0, 0.0

        total_distance = 0.0
        start_time = self.route_points[0][2]
        end_time = self.route_points[-1][2]

        for i in range(len(self.route_points) - 1):
            p1 = (self.route_points[i][0], self.route_points[i][1])
            p2 = (self.route_points[i+1][0], self.route_points[i+1][1])
            total_distance += self.haversine_distance(p1, p2)

        duration_hours = (end_time - start_time).total_seconds() / 3600
        avg_speed = total_distance / duration_hours if duration_hours > 0 else 0.0

        return round(total_distance, 2), round(avg_speed, 2)

    def run_simulation(self):
        print("--- Physical Activity Tracker ---")
        print("Activity started: Running")
        
        # Simulated route (e.g., small increments in New York City)
        start_lat, start_lon = 40.730610, -73.935242
        
        for i in range(5):
            current_lat = start_lat + (i * 0.001)
            current_lon = start_lon + (i * 0.001)
            self.record_waypoint(current_lat, current_lon)
            print(f"Ping {i+1}: Lat {current_lat:.6f}, Lon {current_lon:.6f}")
            time.sleep(1) # Simulating time gap between pings

        distance, speed = self.calculate_metrics()
        
        print("-" * 30)
        print(f"Activity Summary:")
        print(f"Total Distance: {distance} km")
        print(f"Average Speed: {speed} km/h")
        print("-" * 30)

if __name__ == "__main__":
    tracker = ActivityTracker()
    tracker.run_simulation()