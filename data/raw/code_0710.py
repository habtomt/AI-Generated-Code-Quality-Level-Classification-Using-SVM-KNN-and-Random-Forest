"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries
import requests
import json
import schedule
import time
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Replace with your API key
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

# Function to get current weather
def get_current_weather(city, api_key):
    """
    Get current weather for a given city using OpenWeatherMap API.
    
    Parameters:
    city (str): City name
    api_key (str): OpenWeatherMap API key
    
    Returns:
    dict: Current weather data
    """
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Function to get forecasted weather
def get_forecasted_weather(city, api_key):
    """
    Get forecasted weather for a given city using OpenWeatherMap API.
    
    Parameters:
    city (str): City name
    api_key (str): OpenWeatherMap API key
    
    Returns:
    dict: Forecasted weather data
    """
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Function to send notification via email
def send_notification(subject, message, to_email):
    """
    Send notification via email using SMTP.
    
    Parameters:
    subject (str): Email subject
    message (str): Email body
    to_email (str): Recipient email address
    """
    # Replace with your email credentials
    sender_email = "YOUR_EMAIL"
    sender_password = "YOUR_PASSWORD"
    
    # Set up email server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls(context=ssl.create_default_context())
    server.login(sender_email, sender_password)
    
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    text = msg.as_string()
    server.sendmail(sender_email, to_email, text)
    server.quit()

# Main function
def main():
    # Replace with your city and email address
    city = "New York"
    to_email = "RECIPIENT_EMAIL"
    
    # Get current and forecasted weather
    current_weather = get_current_weather(city, API_KEY)
    forecasted_weather = get_forecasted_weather(city, API_KEY)
    
    # Check for severe weather
    if current_weather:
        weather_condition = current_weather['weather'][0]['description']
        if "rain" in weather_condition.lower() or "thunderstorm" in weather_condition.lower():
            send_notification("Severe Weather Alert", f"Severe weather detected in {city}. Current weather: {weather_condition}", to_email)
    
    if forecasted_weather:
        for forecast in forecasted_weather['list']:
            forecasted_condition = forecast['weather'][0]['description']
            if "rain" in forecasted_condition.lower() or "thunderstorm" in forecasted_condition.lower():
                send_notification("Severe Weather Alert", f"Severe weather forecasted in {city} at {forecast['dt_txt']}. Forecasted weather: {forecasted_condition}", to_email)

# Schedule main function to run every hour
schedule.every(1).hours.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)