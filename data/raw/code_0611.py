"""
Auto-generated Python code
Scenario : Social Media Integration
Prompt   : response_000.txt
Run      : 3
"""

# Import required libraries
import requests
import json
import os
from flask import Flask, redirect, url_for, request
from flask_session import Session
from flask import session
from oauthlib.common import generate_token
from flask_oauth import OAuth

# Initialize Flask application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Social media platform credentials
fb_app_id = "YOUR_FB_APP_ID"  # Facebook App ID
fb_app_secret = "YOUR_FB_APP_SECRET"  # Facebook App Secret
google_app_id = "YOUR_GOOGLE_APP_ID"  # Google App ID
google_app_secret = "YOUR_GOOGLE_APP_SECRET"  # Google App Secret

# Set up OAuth for Facebook and Google
facebook = OAuth(app, consumer_key=fb_app_id, consumer_secret=fb_app_secret, 
                 request_token_params={'scope': 'email'}, base_url='https://graph.facebook.com')
google = OAuth(app, consumer_key=google_app_id, consumer_secret=google_app_secret, 
               request_token_params={'scope': 'email'}, base_url='https://accounts.google.com')

# Route for Facebook login
@app.route("/facebook")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                              _external=True))

# Callback function for Facebook login
@app.route("/facebook/authorized")
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = requests.get('https://graph.facebook.com/me?fields=id,email,name&access_token=' + resp['access_token']).json()
    user_id = me['id']
    user_email = me['email']
    user_name = me['name']
    # Create or update user profile in your application
    # Replace this with your own logic
    create_or_update_user_profile(user_id, user_email, user_name)
    return jsonify({'message': 'User logged in successfully'}), 200

# Route for Google login
@app.route("/google")
def google_login():
    return google.authorize(callback=url_for('google_authorized',
                                             _external=True))

# Callback function for Google login
@app.route("/google/authorized")
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = requests.get('https://www.googleapis.com/plus/v1/people/me?access_token=' + resp['access_token']).json()
    user_id = me['id']
    user_email = me['email']
    user_name = me['name']
    # Create or update user profile in your application
    # Replace this with your own logic
    create_or_update_user_profile(user_id, user_email, user_name)
    return jsonify({'message': 'User logged in successfully'}), 200

# Helper function to create or update user profile
def create_or_update_user_profile(user_id, user_email, user_name):
    # Replace this with your own logic
    print(f'Creating or updating user profile for {user_id} with email {user_email} and name {user_name}')

# OAuth callback for Facebook
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

# OAuth callback for Google
@google.tokengetter
def get_google_oauth_token():
    return session.get('oauth_token')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)