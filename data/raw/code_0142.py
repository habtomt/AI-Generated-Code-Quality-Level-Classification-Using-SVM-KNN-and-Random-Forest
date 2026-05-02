# farmer_advisory_app.py

import requests
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"

CROP_RULES = {
    "wheat": {"min_temp": 10, "max_temp": 30, "max_rain": 5},
    "corn": {"min_temp": 15, "max_temp": 35, "max_rain": 8},
    "rice": {"min_temp": 20, "max_temp": 35, "max_rain": 15},
}


def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max"
        ],
        "forecast_days": 7,
        "timezone": "auto"
    }

    data = requests.get(API_URL, params=params).json()
    return data["daily"]


def analyze_for_crop(weather, crop):
    rules = CROP_RULES.get(crop.lower())

    if not rules:
        return ["No rules available for selected crop"]

    advice = []

    temps_max = weather["temperature_2m_max"]
    temps_min = weather["temperature_2m_min"]
    rain = weather["precipitation_sum"]

    for i in range(len(temps_max)):
        tmax = temps_max[i]
        tmin = temps_min[i]
        r = rain[i]

        date = weather["time"][i]

        if tmin < rules["min_temp"]:
            advice.append(f"{date}: ❄ Cold risk - protect crops")

        if tmax > rules["max_temp"]:
            advice.append(f"{date}: 🔥 Heat risk - increase irrigation/shade")

        if r > rules["max_rain"]:
            advice.append(f"{date}: 🌧 Heavy rain - risk of flooding/disease")

        if rules["min_temp"] <= tmin <= rules["max_temp"] and r < rules["max_rain"]:
            advice.append(f"{date}: ✅ Good conditions for crop activity")

    return advice


def planting_harvesting_tip(weather):
    avg_temp = sum(weather["temperature_2m_max"]) / len(weather["temperature_2m_max"])
    total_rain = sum(weather["precipitation_sum"])

    if avg_temp > 20 and total_rain < 20:
        return "🌱 Good period for planting"
    elif total_rain > 30:
        return "⚠ Delay planting/harvesting due to rain"
    else:
        return "📊 Moderate conditions"


def main():
    print("🌾 Farmer Advisory System")

    lat = float(input("Enter latitude: ") or 41.0082)
    lon = float(input("Enter longitude: ") or 28.9784)

    crop = input("Enter crop type (wheat/corn/rice): ")

    weather = fetch_weather(lat, lon)

    print("\n📅 Weather-based Agricultural Advice:\n")

    crop_advice = analyze_for_crop(weather, crop)

    for a in crop_advice:
        print(a)

    print("\n🧠 General Recommendation:")
    print(planting_harvesting_tip(weather))


if __name__ == "__main__":
    main()