# weather_alert_monitor.py

import requests
import time
import smtplib
from email.mime.text import MIMEText

API_URL = "https://api.open-meteo.com/v1/forecast"

LATITUDE = 41.0082
LONGITUDE = 28.9784

CHECK_INTERVAL = 300  # seconds (5 minutes)

ALERT_TEMP_THRESHOLD = 35
ALERT_WIND_THRESHOLD = 60
ALERT_PRECIP_THRESHOLD = 20


EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"


def fetch_weather():
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current_weather": True,
        "hourly": "precipitation"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    current = data["current_weather"]

    weather = {
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "time": current["time"]
    }

    return weather


def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


def check_alert_conditions(weather):
    alerts = []

    if weather["temperature"] >= ALERT_TEMP_THRESHOLD:
        alerts.append(f"High temperature detected: {weather['temperature']}°C")

    if weather["windspeed"] >= ALERT_WIND_THRESHOLD:
        alerts.append(f"Strong wind detected: {weather['windspeed']} km/h")

    return alerts


def monitor_weather():
    print("Weather monitoring started...")

    while True:
        try:
            weather = fetch_weather()
            print(f"Current weather: {weather}")

            alerts = check_alert_conditions(weather)

            if alerts:
                message = "\n".join(alerts)
                send_email_alert("Severe Weather Alert", message)
                print("Alert sent!")

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_weather()