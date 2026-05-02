"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_003.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from social_platforms import get_facebook_data, get_twitter_data, get_instagram_data

# Function to get social media analytics data
def get_social_media_data():
    try:
        # Get Facebook analytics data
        facebook_data = get_facebook_data(api_key="YOUR_FACEBOOK_API_KEY")
        
        # Get Twitter analytics data
        twitter_data = get_twitter_data(api_key="YOUR_TWITTER_API_KEY")
        
        # Get Instagram analytics data
        instagram_data = get_instagram_data(api_key="YOUR_INSTAGRAM_API_KEY")
        
        # Combine data into a single DataFrame
        data = pd.concat([facebook_data, twitter_data, instagram_data])
        
        return data
    
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to create dashboard
def create_dashboard(data):
    try:
        # Create a new figure
        fig, axs = plt.subplots(3, figsize=(10, 10))
        
        # Plot user engagement over time
        sns.lineplot(data=data, x="date", y="engagement", ax=axs[0])
        axs[0].set_title("User Engagement Over Time")
        
        # Plot follower growth over time
        sns.lineplot(data=data, x="date", y="followers", ax=axs[1])
        axs[1].set_title("Follower Growth Over Time")
        
        # Plot post performance metrics
        sns.barplot(data=data, x="post_type", y="performance", ax=axs[2])
        axs[2].set_title("Post Performance Metrics")
        
        # Display the plot
        plt.tight_layout()
        plt.show()
        
        # Create a new figure for plotly
        fig = px.bar(data, x="post_type", y="performance")
        
        # Display the plot
        fig.show()
    
    except Exception as e:
        print(f"Error: {e}")

# Get social media analytics data
data = get_social_media_data()

# Create dashboard
create_dashboard(data)