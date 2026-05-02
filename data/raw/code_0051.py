#!/usr/bin/env python3

import requests
import math
from typing import List, Dict, Any

IP_GEO_URL = "http://ip-api.com/json/"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_location() -> Dict[str, float]:
    resp = requests.get(IP_GEO_URL, timeout=10)
    data = resp.json()
    return {
        "lat": data.get("lat", 0.0),
        "lon": data.get("lon", 0.0),
        "city": data.get("city", ""),
        "country": data.get("country", "")
    }


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def fetch_nearby_businesses(lat: float, lon: float) -> List[Dict[str, Any]]:
    query = f"""
    [out:json];
    (
      node["amenity"](around:3000,{lat},{lon});
      way["amenity"](around:3000,{lat},{lon});
      relation["amenity"](around:3000,{lat},{lon});
    );
    out center 20;
    """

    resp = requests.post(OVERPASS_URL, data=query, timeout=30)
    data = resp.json()

    businesses = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name")
        if not name:
            continue

        el_lat = el.get("lat") or el.get("center", {}).get("lat")
        el_lon = el.get("lon") or el.get("center", {}).get("lon")

        if el_lat is None or el_lon is None:
            continue

        dist = haversine(lat, lon, el_lat, el_lon)

        businesses.append({
            "name": name,
            "lat": el_lat,
            "lon": el_lon,
            "distance_km": dist,
            "type": tags.get("amenity", "unknown")
        })

    businesses.sort(key=lambda x: x["distance_km"])
    return businesses[:20]


def generate_ads(businesses: List[Dict[str, Any]]) -> List[str]:
    ads = []
    for b in businesses[:10]:
        ads.append(f"🔥 Special offer near you: {b['name']} ({b['type']}) - only {b['distance_km']:.2f} km away!")
    return ads


def main():
    loc = get_location()

    print(f"Detected location: {loc['city']}, {loc['country']} ({loc['lat']}, {loc['lon']})")

    businesses = fetch_nearby_businesses(loc["lat"], loc["lon"])

    if not businesses:
        print("No nearby businesses found.")
        return

    ads = generate_ads(businesses)

    print("\n--- Targeted Ads ---")
    for ad in ads:
        print(ad)


if __name__ == "__main__":
    main()