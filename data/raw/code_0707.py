"""
Auto-generated Python code
Scenario : Weather Data
Prompt   : response_004.txt
Run      : 1
"""

# Import necessary libraries
import requests
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Create a new Flask app
app = Flask(__name__)

# Mongodb database setup
MONGO_URI = "mongodb+srv://YOUR_MONGODB_USERNAME:YOUR_MONGODB_PASSWORD@YOUR_CLUSTER_NAME/YOUR_DB_NAME"
client = MongoClient(MONGO_URI)
db = client["your_db_name"]

# API key for weatherapi
API_KEY = "YOUR_WEATHER_API_KEY"

# Function to get weather data from weatherapi
def get_weather_data(location):
    try:
        response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=5")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Function to generate recommendation based on weather data
def generate_recommendation(forecast):
    try:
        if forecast["forecast"]["forecastday"][0]["day"]["condition"]["text"].lower().includes("rain"):
            return "Prepare for rain, consider delaying planting."
        elif forecast["forecast"]["forecastday"][0]["day"]["avgtemp_c"] > 30:
            return "High temperatures, increase irrigation."
        else:
            return "General recommendations..."
    except Exception as e:
        return {"error": str(e)}

# Route to handle form submission
@app.route('/getAdvice', methods=['POST'])
def get_advice():
    try:
        location = request.json["location"]
        crops = request.json["crops"]
        user_data = {
            "location": location,
            "crops": crops
        }
        db.users.insert_one(user_data)
        weather_data = get_weather_data(location)
        recommendation = generate_recommendation(weather_data)
        return jsonify({"weather_data": weather_data, "recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve form
@app.route('/')
def index():
    return """
    <html>
    <body>
    <h1>Farming Advisory Application</h1>
    <form id="inputForm" method="POST">
        <label for="location">Location:</label>
        <input type="text" id="location" name="location" required><br><br>
        
        <label for="crops">Type of Crops:</label>
        <input type="text" id="crops" name="crops" required><br><br>

        <button type="submit">Get Advice</button>
    </form>

    <div id="results"></div>

    <script>
        document.getElementById('inputForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const location = document.getElementById('location').value;
            const crops = document.getElementById('crops').value;

            try {
                const response = await fetch('/getAdvice', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ location, crops }),
                });

                const data = await response.json();
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = `<h2>Weather Forecast</h2><pre>${JSON.stringify(data.weather_data, null, 2)}</pre>
                                        <h2>Recommendation</h2><p>${data.recommendation}</p>`;
            } catch (err) {
                console.error('Error fetching advice:', err);
            }
        });
    </script>
    </body>
    </html>
    """

# Run the app
if __name__ == "__main__":
    app.run(debug=True)