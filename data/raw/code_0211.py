import math
import time
import random

class ARNavigationSystem:
    def __init__(self):
        self.camera_active = False
        self.current_coords = (40.7484, -73.9857)  # Example: Empire State Building
        self.destination_coords = (40.7527, -73.9772)  # Example: Grand Central Terminal
        self.viewport_width = 1920
        self.viewport_height = 1080

    def get_bearing(self, lat1, lon1, lat2, lon2):
        """
        Calculates the forward azimuth between two points.
        """
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        d_lon = lon2 - lon1
        y = math.sin(d_lon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
        bearing = math.atan2(y, x)
        return (math.degrees(bearing) + 360) % 360

    def get_device_orientation(self):
        """
        Simulates data from Magnetometer and Gyroscope.
        Returns degrees from North.
        """
        return random.uniform(0, 360)

    def calculate_ar_overlay_position(self, target_bearing, current_heading):
        """
        Maps a geographic bearing to screen coordinates on the camera feed.
        """
        relative_angle = (target_bearing - current_heading + 180) % 360 - 180
        
        # Simple Projection: If target is within 45 degree Field of View (FOV)
        fov = 90
        if abs(relative_angle) <= fov / 2:
            x_pos = (self.viewport_width / 2) + (relative_angle * (self.viewport_width / fov))
            return int(x_pos), self.viewport_height // 2
        return None

    def start_ar_session(self):
        self.camera_active = True
        print(f"--- AR Navigation Initialized ---")
        print(f"Destination: {self.destination_coords}")
        
        try:
            for _ in range(10):
                heading = self.get_device_orientation()
                bearing = self.get_bearing(
                    self.current_coords[0], self.current_coords[1],
                    self.destination_coords[0], self.destination_coords[1]
                )
                
                screen_coords = self.calculate_ar_overlay_position(bearing, heading)
                
                print(f"[Sensors] Heading: {heading:.2f}° | Bearing to Target: {bearing:.2f}°")
                
                if screen_coords:
                    print(f" >> OVERLAY: Rendering 'Turn Right' Arrow at screen coordinates: {screen_coords}")
                else:
                    print(" >> OVERLAY: Destination outside camera FOV. Rotate device.")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.camera_active = False

if __name__ == "__main__":
    ar_nav = ARNavigationSystem()
    ar_nav.start_ar_session()