import os
from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'DEVELOPMENT_SECRET_KEY' # Replace with a secure key

# OAuth Configuration
oauth = OAuth(app)

# Example: Registering GitHub as the Social Provider
# In a real app, you would get CLIENT_ID and CLIENT_SECRET from the developer dashboard
github = oauth.register(
    name='github',
    client_id='YOUR_GITHUB_CLIENT_ID',
    client_secret='YOUR_GITHUB_CLIENT_SECRET',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Mock Database for User Profiles
users_db = {}

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Hello, {user["name"]}! <a href="/logout">Logout</a>'
    return '<a href="/login">Login with GitHub</a>'

@app.route('/login')
def login():
    # Redirect user to GitHub's OAuth page
    redirect_uri = url_for('auth_callback', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    # Receive the access token
    token = github.authorize_access_token()
    
    # Retrieve user information from the provider's API
    resp = github.get('user')
    profile = resp.json()
    
    # Logic to Create or Update User Profile
    user_id = str(profile.get('id'))
    user_data = {
        'id': user_id,
        'name': profile.get('name') or profile.get('login'),
        'email': profile.get('email'),
        'avatar': profile.get('avatar_url')
    }
    
    # Save/Update in "Database"
    users_db[user_id] = user_data
    
    # Store user in session
    session['user'] = user_data
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    # To run this locally, you must install: pip install Flask Authlib requests
    app.run(debug=True, port=5000)