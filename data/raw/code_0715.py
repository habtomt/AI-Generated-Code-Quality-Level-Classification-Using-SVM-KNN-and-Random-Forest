"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_002.txt
Run      : 3
"""

# Import required libraries
import requests
import json
import schedule
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Replace with your OpenWeatherMap API key
API_KEY = 'YOUR_API_KEY'

# Replace with your email credentials
FROM_EMAIL = 'YOUR_EMAIL'
PASSWORD = 'YOUR_PASSWORD'
TO_EMAIL = 'USER_EMAIL'

def get_weather_data(city, api_key):
    """
    Retrieves current weather data from OpenWeatherMap API.
    
    Args:
    city (str): City name.
    api_key (str): OpenWeatherMap API key.
    
    Returns:
    dict: Current weather data.
    """
    try:
        # Construct API URL
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        # Send GET request
        response = requests.get(url)
        
        # Return JSON response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

def check_weather(weather_data):
    """
    Checks if weather conditions are severe.
    
    Args:
    weather_data (dict): Current weather data.
    
    Returns:
    bool: True if severe weather, False otherwise.
    """
    # Check if weather data is available
    if weather_data:
        # Check for severe weather conditions (wind speed > 64 km/h, rain probability > 50%)
        if weather_data['wind']['speed'] > 64 or weather_data['rain'] > 50:
            return True
        return False
    return False

def send_notification(subject, message):
    """
    Sends email notification to user.
    
    Args:
    subject (str): Email subject.
    message (str): Email message.
    """
    try:
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email using SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, TO_EMAIL, text)
        server.quit()
        print('Notification sent successfully.')
    except Exception as e:
        print(f'Error: {e}')

def monitor_weather(city):
    """
    Monitors weather conditions and sends notifications when severe weather is detected or forecasted.
    
    Args:
    city (str): City name.
    """
    # Get current weather data
    weather_data = get_weather_data(city, API_KEY)
    
    # Check if severe weather is detected
    if check_weather(weather_data):
        # Send notification
        send_notification('Severe Weather Alert', f'Severe weather detected in {city}.')
    
    # Schedule next weather check
    schedule.every(1).hours.do(monitor_weather, city)  # Check every hour

def main():
    # Start monitoring weather
    monitor_weather('London')  # Replace with your city name
    
    # Run schedule indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Start main program
    main()