"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_002.txt
Run      : 3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from datetime import datetime, timedelta
import warnings
import requests
import json

# Set warnings to ignore
warnings.filterwarnings("ignore")

# Set API key for Google Analytics
GA_API_KEY = "YOUR_GA_API_KEY"

# Set view ID for Google Analytics
VIEW_ID = "YOUR_VIEW_ID"

# Function to fetch data from Google Analytics API
def fetch_data(api_key, view_id):
    try:
        url = f"https://analyticsdata.googleapis.com/v1alpha/properties/{view_id}/metrics/rt:activeUsers,rt:screenPageViews,rt:screenBounceRate,rt:screenEngagedSessions,rt:activeUsers,rt:sessionDuration,rt:screenEngagedUsers,rt:sessionCount,rt:screenEngagedTimePerSession"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")

# Function to process data
def process_data(data):
    try:
        # Create a Pandas DataFrame
        df = pd.json_normalize(data["reports"][0]["data"]["rows"])

        # Convert timestamp to datetime
        df["timestamp"] = pd.to_datetime(df["metricValues"][0]["value"], unit="s")

        # Extract relevant columns
        df = df[["timestamp", "metricValues"][0]["value"]]

        # Rename columns
        df.columns = ["timestamp", "active_users"]
        df["date"] = df["timestamp"].dt.date

        # Group by date and calculate sum
        df = df.groupby("date")["active_users"].sum().reset_index()

        # Plot data
        plt.figure(figsize=(10, 6))
        sns.lineplot(x="date", y="active_users", data=df)
        plt.title("Active Users Over Time")
        plt.show()

        # Identify peak traffic times
        peak_traffic_time = df["date"].loc[df["active_users"].idxmax()]
        print(f"Peak traffic time: {peak_traffic_time}")

        # Calculate user demographics
        user_demographics = df["active_users"].mean()
        print(f"Average active users: {user_demographics}")

        # Calculate engagement metrics
        engagement_metrics = df["active_users"].std()
        print(f"Standard deviation of active users: {engagement_metrics}")

        # Create a scatter plot
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="date", y="active_users", data=df)
        plt.title("Active Users Over Time")
        plt.show()
    except Exception as e:
        print(f"Error processing data: {e}")

# Fetch data from Google Analytics API
data = fetch_data(GA_API_KEY, VIEW_ID)

# Process data
process_data(data)