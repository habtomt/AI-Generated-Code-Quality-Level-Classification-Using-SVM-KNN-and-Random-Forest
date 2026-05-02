import os
import requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- Configuration ---
# In a production environment, these would be stored in environment variables
ACCESS_TOKEN = 'YOUR_SOCIAL_MEDIA_ACCESS_TOKEN'
API_FEED_URL = 'https://api.socialprovider.com/v1/me/feed' 

# --- HTML Template for Rendering Feed ---
FEED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Social Media Feed</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
        .feed-container { max-width: 600px; margin: auto; }
        .post { background: white; border: 1px solid #ddd; margin-bottom: 20px; padding: 15px; border-radius: 8px; }
        .post img, .post video { max-width: 100%; border-radius: 4px; margin-top: 10px; }
        .post-header { font-weight: bold; margin-bottom: 10px; color: #333; }
        .post-content { color: #555; line-height: 1.4; }
        .timestamp { font-size: 0.8em; color: #999; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="feed-container">
        <h1>Your Feed</h1>
        {% for post in posts %}
        <div class="post">
            <div class="post-header">{{ post.author }}</div>
            <div class="post-content">{{ post.text }}</div>
            
            {% if post.media_type == 'image' %}
                <img src="{{ post.media_url }}" alt="Post image">
            {% elif post.media_type == 'video' %}
                <video controls>
                    <source src="{{ post.media_url }}" type="video/mp4">
                </video>
            {% endif %}
            
            <div class="timestamp">{{ post.created_at }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

def fetch_social_feed():
    """
    Simulates fetching data from an external Social Media API.
    """
    try:
        # Example API Call
        # response = requests.get(API_FEED_URL, headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
        # response.raise_for_status()
        # return response.json()
        
        # Mocked data structure based on typical social API responses
        return [
            {
                "id": "1",
                "author": "TechInnovator",
                "text": "Just launched our new Python-based API! 🚀 #Python #Coding",
                "media_type": "image",
                "media_url": "https://via.placeholder.com/600x400?text=New+API+Launch",
                "created_at": "2026-04-23 10:00"
            },
            {
                "id": "2",
                "author": "NatureDaily",
                "text": "A beautiful morning in the mountains. Check out this view!",
                "media_type": "video",
                "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
                "created_at": "2026-04-23 08:30"
            },
            {
                "id": "3",
                "author": "CodeGuru",
                "text": "Clean code is not written; it is written and rewritten. Keep refactoring.",
                "media_type": "text",
                "media_url": None,
                "created_at": "2026-04-22 15:45"
            }
        ]
    except Exception as e:
        print(f"Error fetching feed: {e}")
        return []

@app.route('/')
def display_feed():
    posts = fetch_social_feed()
    return render_template_string(FEED_TEMPLATE, posts=posts)

@app.route('/api/raw-feed')
def raw_feed():
    posts = fetch_social_feed()
    return jsonify(posts)

if __name__ == '__main__':
    # Required: pip install Flask requests
    app.run(debug=True, port=5000)