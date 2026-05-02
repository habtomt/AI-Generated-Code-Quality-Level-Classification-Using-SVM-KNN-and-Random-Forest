"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
from datetime import datetime

# Sample marketing campaign data (replace with actual data)
data = {
    "Campaign ID": [1, 1, 1, 2, 2, 2, 3, 3, 3],
    "Date": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", "2022-01-07", "2022-01-08", "2022-01-09"],
    "Impressions": [100, 120, 110, 130, 140, 150, 160, 170, 180],
    "Clicks": [5, 6, 7, 8, 9, 10, 11, 12, 13],
    "Conversions": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Revenue": [100, 120, 110, 130, 140, 150, 160, 170, 180],
    "Cost": [20, 25, 30, 35, 40, 45, 50, 55, 60]
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Calculate the conversion rate (Conversions / Clicks)
df['Conversion Rate'] = df['Conversions'] / df['Clicks']

# Calculate the ROI (Return on Investment) - (Revenue - Cost) / Cost
df['ROI'] = ((df['Revenue'] - df['Cost']) / df['Cost']) * 100

# Calculate the customer engagement (Clicks / Impressions)
df['Customer Engagement'] = df['Clicks'] / df['Impressions']

# Print the DataFrame with the calculated KPIs
print(df)

# Group the data by Campaign ID and calculate the average KPIs
average_kpis = df.groupby('Campaign ID').mean().reset_index()

# Print the average KPIs for each campaign
print(average_kpis)

# Define a function to calculate the campaign effectiveness score
def calculate_campaign_effectiveness(campaign_id):
    # Filter the data for the specified campaign
    campaign_data = df[df['Campaign ID'] == campaign_id]
    
    # Calculate the weighted average of the KPIs
    effectiveness_score = (campaign_data['Conversion Rate'].mean() + campaign_data['ROI'].mean() + campaign_data['Customer Engagement'].mean()) / 3
    
    return effectiveness_score

# Test the function with a specific campaign ID
print(calculate_campaign_effectiveness(1))