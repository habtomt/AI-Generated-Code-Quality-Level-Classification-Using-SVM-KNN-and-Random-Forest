import requests
from datetime import datetime

# Configuration
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with a valid API key
CITY = "Central Valley"  # Example agricultural hub

class FarmingAdvisory:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def fetch_forecast(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def generate_recommendations(self, data):
        advisories = []
        # Group by day for simplified daily guidance
        daily_summary = {}

        for entry in data['list']:
            date = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')
            if date not in daily_summary:
                daily_summary[date] = {
                    "temps": [],
                    "humidity": [],
                    "wind": [],
                    "rain": False,
                    "desc": entry['weather'][0]['main']
                }
            
            daily_summary[date]["temps"].append(entry['main']['temp'])
            daily_summary[date]["humidity"].append(entry['main']['humidity'])
            daily_summary[date]["wind"].append(entry['wind']['speed'])
            if "Rain" in entry['weather'][0]['main']:
                daily_summary[date]["rain"] = True

        for day, stats in daily_summary.items():
            avg_temp = sum(stats["temps"]) / len(stats["temps"])
            avg_hum = sum(stats["humidity"]) / len(stats["humidity"])
            max_wind = max(stats["wind"])
            
            tips = []
            
            # 1. Planting Advisory
            if 15 <= avg_temp <= 25 and not stats["rain"]:
                tips.append("[PLANTING] Optimal conditions for sowing. Soil temperature and moisture are favorable.")
            elif avg_temp < 5:
                tips.append("[PLANTING] Risk of frost. Delay planting sensitive seeds.")

            # 2. Harvesting Advisory
            if not stats["rain"] and avg_hum < 60:
                tips.append("[HARVEST] Excellent window for harvesting and dry storage.")
            elif stats["rain"]:
                tips.append("[HARVEST] Avoid harvesting; moisture levels will lead to fungal growth/spoilage.")

            # 3. Protection & Spraying
            if max_wind > 5:
                tips.append("[SPRAYING] High wind detected. Do not apply pesticides/fertilizers to avoid drift.")
            elif stats["rain"]:
                tips.append("[PROTECTION] Incoming rain detected. Do not spray chemicals as they will wash away.")
            
            # 4. Irrigation
            if stats["rain"]:
                tips.append("[IRRIGATION] Natural precipitation expected. Suspend automated irrigation to save water.")
            elif avg_temp > 30:
                tips.append("[IRRIGATION] High heat. Increase water supply to prevent heat stress.")

            advisories.append({
                "date": day,
                "avg_temp": round(avg_temp, 1),
                "condition": stats["desc"],
                "recommendations": tips
            })

        return advisories

def main():
    advisor = FarmingAdvisory(API_KEY)
    
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        print("Please update the script with your API Key.")
        return

    print(f"--- Agricultural Advisory Report for {CITY} ---")
    weather_data = advisor.fetch_forecast(CITY)
    
    if weather_data:
        reports = advisor.generate_recommendations(weather_data)
        
        for report in reports[:5]:  # Display next 5 days
            print(f"\nDATE: {report['date']} | {report['avg_temp']}°C | {report['condition']}")
            if report['recommendations']:
                for rec in report['recommendations']:
                    print(f"  - {rec}")
            else:
                print("  - Conditions stable. Proceed with standard maintenance.")

if __name__ == "__main__":
    main()