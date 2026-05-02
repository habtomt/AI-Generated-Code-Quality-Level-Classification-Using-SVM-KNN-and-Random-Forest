import requests
import time
import json
from datetime import datetime

# Configuration
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual API key
LAT = "40.7128"                          # Latitude for New York (Example)
LON = "-74.0060"                         # Longitude for New York (Example)
CHECK_INTERVAL = 300                     # Check every 5 minutes (300 seconds)

def fetch_weather_alerts():
    """
    Fetches weather data including government-issued alerts using the One Call API.
    Note: Requires a subscription to One Call API 3.0 (often includes a free tier).
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude=minutely,hourly,daily&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("alerts", [])
    except Exception as e:
        print(f"[{datetime.now()}] Connection Error: {e}")
        return []

def send_notification(alert):
    """
    Simulates sending a notification. 
    In a production app, this could trigger an Email, SMS, or Push Notification.
    """
    sender = alert.get("sender_name", "National Weather Service")
    event = alert.get("event", "Severe Weather Warning")
    description = alert.get("description", "No details provided.")
    start = datetime.fromtimestamp(alert.get("start")).strftime('%Y-%m-%d %H:%M')
    end = datetime.fromtimestamp(alert.get("end")).strftime('%Y-%m-%d %H:%M')

    print("\n" + "!" * 50)
    print(f"!!! SEVERE WEATHER ALERT DETECTED !!!")
    print(f"Source:  {sender}")
    print(f"Event:   {event}")
    print(f"Period:  {start} to {end}")
    print(f"Details: {description[:200]}...") # Truncated for readability
    print("!" * 50 + "\n")

def monitor_loop():
    """
    Continuously monitors weather conditions.
    """
    known_alerts = set()
    
    print(f"Starting Weather Monitor for Lat: {LAT}, Lon: {LON}...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            alerts = fetch_weather_alerts()
            
            if not alerts:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No severe weather alerts in your area.")
            else:
                for alert in alerts:
                    # Use a combination of event and start time as a unique ID
                    alert_id = f"{alert.get('event')}_{alert.get('start')}"
                    
                    if alert_id not in known_alerts:
                        send_notification(alert)
                        known_alerts.add(alert_id)
            
            # Clean up old alerts from the set to prevent memory leak over long periods
            if len(known_alerts) > 100:
                known_alerts.clear()

            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        print("Error: Please set your OpenWeatherMap API Key in the script.")
    else:
        monitor_loop()