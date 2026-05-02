"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
import os
import json
import requests
from flask import Flask, request, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
Session(app)
db = SQLAlchemy(app)

# OAuth settings for social media platforms
oauth = OAuth(app)

# Google OAuth settings
google = oauth.remote_app(
    'google',
    consumer_key='YOUR_GOOGLE_CLIENT_ID',
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={'scope': 'email profile'},
    base_url='https://www.googleapis.com/oauth2/v2/',
    request_token_url=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_method='POST',
    response_method='json'
)

# Facebook OAuth settings
facebook = oauth.remote_app(
    'facebook',
    consumer_key='YOUR_FACEBOOK_CLIENT_ID',
    consumer_secret='YOUR_FACEBOOK_CLIENT_SECRET',
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='https://graph.facebook.com/oauth/access_token',
    access_token_method='GET',
    response_method='json'
)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(120))

# Route for Google OAuth
@app.route('/login/google')
def google_login():
    try:
        return google.authorize(callback=url_for('authorized', _external=True))
    except Exception as e:
        print(f"Error in Google login: {e}")

# Route for Google OAuth authorization
@app.route('/login/authorized')
def authorized():
    try:
        resp = google.authorized_response()
        if resp is None:
            return 'Access denied: reason={} error={}'.format(
                request.args['error_reason'],
                request.args['error_description']
            )
        session['oauth_token'] = (resp['access_token'], '')
        me = google.get('user').data
        username = me['name']
        email = me['email']
        profile_picture = me['picture']['url']
        
        # Check if user exists, if not create a new one
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(username=username, email=email, profile_picture=profile_picture)
            db.session.add(user)
            db.session.commit()
        
        # Login user
        session['username'] = username
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error in Google authorization: {e}")
        return 'Error'

# Route for Facebook OAuth
@app.route('/login/facebook')
def facebook_login():
    try:
        return facebook.authorize(callback=url_for('authorized_facebook', _external=True))
    except Exception as e:
        print(f"Error in Facebook login: {e}")

# Route for Facebook OAuth authorization
@app.route('/login/authorized_facebook')
def authorized_facebook():
    try:
        resp = facebook.authorized_response()
        if resp is None:
            return 'Access denied: reason={} error={}'.format(
                request.args['error_reason'],
                request.args['error_description']
            )
        session['oauth_token'] = (resp['access_token'], '')
        me = facebook.get('me').data
        username = me['name']
        email = me['email']
        profile_picture = me['picture']['data']['url']
        
        # Check if user exists, if not create a new one
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(username=username, email=email, profile_picture=profile_picture)
            db.session.add(user)
            db.session.commit()
        
        # Login user
        session['username'] = username
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error in Facebook authorization: {e}")
        return 'Error'

# Route for index
@app.route('/')
def index():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    return redirect(url_for('login'))

# Route for login
@app.route('/login')
def login():
    return redirect(url_for('google_login'))

# Google OAuth callback
@google.tokengetter
def get_google_oauth_token():
    return session.get('oauth_token')

# Facebook OAuth callback
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)