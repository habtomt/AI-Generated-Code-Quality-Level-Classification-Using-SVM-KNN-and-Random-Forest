import time
import random
import json
from datetime import datetime

class EmergencyDispatchSystem:
    def __init__(self):
        self.active_incidents = {
            "INC-101": {"lat": 40.748817, "lon": -73.985428, "type": "Fire", "priority": "Critical"},
            "INC-102": {"lat": 40.689247, "lon": -74.044502, "type": "Medical", "priority": "High"}
        }
        self.responders = {
            "UNIT-01": {"lat": 40.7128, "lon": -74.0060, "status": "Available"},
            "UNIT-02": {"lat": 40.7580, "lon": -73.9855, "status": "Available"}
        }

    def get_precise_coordinates(self, unit_id):
        # Simulates fetching GPS/GNSS data from a mobile terminal or vehicle sensor
        # In production, this would interface with hardware APIs or a Webhook
        current_loc = self.responders[unit_id]
        current_loc["lat"] += random.uniform(-0.0005, 0.0005)
        current_loc["lon"] += random.uniform(-0.0005, 0.0005)
        return (current_loc["lat"], current_loc["lon"])

    def calculate_eta(self, start_coords, end_coords):
        # Simplified Haversine/Manhattan distance for navigation logic
        dist = abs(start_coords[0] - end_coords[0]) + abs(start_coords[1] - end_coords[1])
        return round(dist * 1000, 1)  # Simulated minutes

    def stream_tracking_data(self, unit_id, incident_id):
        incident = self.active_incidents.get(incident_id)
        if not incident:
            return

        print(f"--- REAL-TIME TRACKING: {unit_id} to {incident_id} ---")
        print(f"Incident Type: {incident['type']} | Priority: {incident['priority']}")
        
        try:
            for _ in range(5):  # Simulated tracking loop
                current_pos = self.get_precise_coordinates(unit_id)
                eta = self.calculate_eta(current_pos, (incident["lat"], incident["lon"]))
                
                telemetry = {
                    "timestamp": datetime.now().isoformat(),
                    "unit_id": unit_id,
                    "lat": round(current_pos[0], 6),
                    "lon": round(current_pos[1], 6),
                    "eta_minutes": eta
                }
                
                print(f"LAT: {telemetry['lat']} | LON: {telemetry['lon']} | ETA: {telemetry['eta_minutes']} min")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nTracking suspended by Dispatch.")

if __name__ == "__main__":
    system = EmergencyDispatchSystem()
    system.stream_tracking_data("UNIT-01", "INC-101")