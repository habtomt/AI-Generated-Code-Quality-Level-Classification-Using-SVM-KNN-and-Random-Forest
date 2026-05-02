# smart_event_scheduler.py

import requests
from datetime import datetime, timedelta

API_URL = "https://api.open-meteo.com/v1/forecast"

LATITUDE = 41.0082
LONGITUDE = 28.9784


def fetch_forecast():
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": [
            "temperature_2m",
            "precipitation",
            "windspeed_10m"
        ],
        "forecast_days": 7
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    times = data["hourly"]["time"]
    temp = data["hourly"]["temperature_2m"]
    rain = data["hourly"]["precipitation"]
    wind = data["hourly"]["windspeed_10m"]

    forecast = []

    for i in range(len(times)):
        forecast.append({
            "time": times[i],
            "temp": temp[i],
            "rain": rain[i],
            "wind": wind[i]
        })

    return forecast


def score_hour(hour_data):
    score = 100

    if hour_data["temp"] < 5 or hour_data["temp"] > 30:
        score -= 30

    if hour_data["rain"] > 0.5:
        score -= 40

    if hour_data["wind"] > 25:
        score -= 20

    return score


def suggest_best_times(forecast):
    scored = []

    for item in forecast:
        scored.append({
            "time": item["time"],
            "score": score_hour(item),
            "temp": item["temp"],
            "rain": item["rain"],
            "wind": item["wind"]
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:10]


def main():
    print("Smart Event Scheduler")

    event_name = input("Enter event name: ")
    event_date = input("Enter event date (YYYY-MM-DD): ")

    forecast = fetch_forecast()

    suggestions = suggest_best_times(forecast)

    print(f"\nBest time suggestions for '{event_name}':\n")

    for s in suggestions:
        print(
            f"Time: {s['time']} | Score: {s['score']} | "
            f"Temp: {s['temp']}°C | Rain: {s['rain']}mm | Wind: {s['wind']} km/h"
        )

    best = suggestions[0]

    print("\nRecommended slot:")
    print(best["time"])


if __name__ == "__main__":
    main()