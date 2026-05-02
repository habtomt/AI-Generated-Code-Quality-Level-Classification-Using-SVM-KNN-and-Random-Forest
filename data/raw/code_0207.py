import requests
import json

def get_user_location():
    """
    Fetches the user's approximate location based on their public IP address.
    In a production mobile app, you would use GPS coordinates (GPS/GNSS).
    """
    try:
        # Using a free IP Geolocation API
        response = requests.get('https://ipapi.co/json/')
        data = response.json()
        return {
            "lat": data.get("latitude"),
            "lon": data.get("longitude"),
            "city": data.get("city")
        }
    except Exception as e:
        print(f"Error retrieving location: {e}")
        return None

def fetch_nearby_ads(lat, lon):
    """
    Simulates integration with a local business directory/ad server.
    In a real scenario, you would query an API like Google Places or Yelp.
    """
    # Mock database of local businesses and their coordinates
    ad_database = [
        {"business": "Java Junction Coffee", "lat": 40.7128, "lon": -74.0060, "ad": "50% off Lattes! Just 2 blocks away!"},
        {"business": "Tech Gear Hub", "lat": 34.0522, "lon": -118.2437, "ad": "New VR headsets in stock now!"},
        {"business": "The Slice Pizzeria", "lat": 41.8781, "lon": -87.6298, "ad": "Free garlic knots with any large pizza!"}
    ]

    print(f"--- Scanning for deals near {lat}, {lon} ---\n")
    
    # Logic to find the "closest" business (simplified for this example)
    # Real-world apps use the Haversine formula to calculate exact distance
    found_ads = []
    for entry in ad_database:
        # Simple proximity check (roughly within the same general area)
        if abs(entry["lat"] - lat) < 0.5 and abs(entry["lon"] - lon) < 0.5:
            found_ads.append(entry)
    
    return found_ads

def main():
    print("Initializing Proximity Ad Engine...")
    
    location = get_user_location()
    
    if location and location["lat"] and location["lon"]:
        print(f"Location Detected: {location['city']} ({location['lat']}, {location['lon']})")
        
        ads = fetch_nearby_ads(location["lat"], location["lon"])
        
        if ads:
            print("Targeted Advertisements Found:")
            for item in ads:
                print(f"[{item['business']}] -> {item['ad']}")
        else:
            print("No local offers found in your immediate vicinity.")
    else:
        print("Could not determine location. Please check your internet connection.")

if __name__ == "__main__":
    main()