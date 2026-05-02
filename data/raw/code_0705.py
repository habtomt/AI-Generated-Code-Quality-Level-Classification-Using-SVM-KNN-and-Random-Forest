"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_002.txt
Run      : 1
"""

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import os

# Configuration
API_KEY = 'your_openweathermap_api_key'
CITY_ID = 'your_city_id'  # Get the city ID from OpenWeatherMap
SEVERE_WEATHER_CODES = {'Thunderstorm', 'Tornado', 'Squall', 'Extreme'}  # Add more codes as needed
USER_EMAIL = 'user@example.com'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_USERNAME = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'

def fetch_weather_data(city_id, api_key):
    url = f'http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={api_key}'
    response = requests.get(url)
    return response.json()

def check_for_severe_weather(weather_data):
    for entry in weather_data['list']:
        weather = entry['weather'][0]
        if weather['main'] in SEVERE_WEATHER_CODES:
            return weather['description']
    return None

def send_email_notification(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    try:
        weather_data = fetch_weather_data(CITY_ID, API_KEY)
        severe_weather_description = check_for_severe_weather(weather_data)
        
        if severe_weather_description:
            subject = "Severe Weather Alert!"
            body = f"Severe weather detected: {severe_weather_description}. Stay safe!"
            send_email_notification(USER_EMAIL, subject, body)
            print("Severe weather alert sent!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    schedule.every(1).hours.do(main)  # Run the main function every hour

    while True:
        schedule.run_pending()
        time.sleep(1)