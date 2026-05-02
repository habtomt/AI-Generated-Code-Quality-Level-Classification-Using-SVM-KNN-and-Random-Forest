# weather_dashboard.py

import streamlit as st
import requests

def fetch_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    data = response.json()

    current = data["current_condition"][0]

    weather_info = {
        "temperature_C": current["temp_C"],
        "humidity": current["humidity"],
        "wind_speed_kmph": current["windspeedKmph"],
        "description": current["weatherDesc"][0]["value"]
    }

    return weather_info

def main():
    st.set_page_config(page_title="Live Weather Dashboard", layout="centered")

    st.title("🌤 Live Weather Dashboard")

    city = st.text_input("Enter city name:", "Istanbul")

    if st.button("Get Weather"):
        try:
            weather = fetch_weather(city)

            st.subheader(f"Weather in {city}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Temperature (°C)", weather["temperature_C"])

            with col2:
                st.metric("Humidity (%)", weather["humidity"])

            with col3:
                st.metric("Wind Speed (km/h)", weather["wind_speed_kmph"])

            st.write(f"Condition: {weather['description']}")

        except Exception as e:
            st.error(f"Error fetching weather data: {e}")

if __name__ == "__main__":
    main()