"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_001.txt
Run      : 1
"""

# app.py

from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Replace these with the actual API endpoint and your access token
API_ENDPOINT = "https://api.example.com/user/feed"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

@app.route('/')
def show_feed():
    # Fetch data from the social media API
    try:
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
        response = requests.get(API_ENDPOINT, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        feed_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        feed_data = []

    # Pass the data to the template for rendering
    return render_template('feed.html', feed=feed_data)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/callback')
def login_callback():
    code = request.args.get('code')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:5000/login/callback',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    try:
        response = requests.post('https://api.example.com/token', headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_response = response.json()
        ACCESS_TOKEN = token_response['access_token']
        return render_template('feed.html', feed=[])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "Error logging in"

if __name__ == '__main__':
    app.run(debug=True)