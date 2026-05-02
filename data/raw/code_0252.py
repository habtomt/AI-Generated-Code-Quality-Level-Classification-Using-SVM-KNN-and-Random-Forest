import os
from flask import Flask, redirect, url_for, session, request, render_template_string
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- OAuth Configuration ---
# Note: You must register your app on the developer portals of these platforms
oauth = OAuth(app)
oauth.register(
    name='twitter',
    client_id='YOUR_TWITTER_CLIENT_ID',
    client_secret='YOUR_TWITTER_CLIENT_SECRET',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    client_kwargs={'scope': 'tweet.write users.read'},
)

# --- HTML Interface ---
LAYOUT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Social Share Feature</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; padding: 50px; background: #fafafa; }
        .share-card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 400px; }
        textarea { width: 100%; height: 100px; margin-top: 10px; padding: 10px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 5px; }
        .btn { display: block; width: 100%; padding: 12px; margin-top: 15px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; text-align: center; text-decoration: none; }
        .btn-twitter { background-color: #1DA1F2; color: white; }
        .status { margin-top: 15px; padding: 10px; border-radius: 5px; background: #e8f5e9; color: #2e7d32; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="share-card">
        <h2>Share to Social Media</h2>
        <form action="/share" method="post">
            <label>What's on your mind?</label>
            <textarea name="content" placeholder="Write something amazing...">I just discovered this cool feature in my new Python app! 🚀</textarea>
            
            {% if not logged_in %}
                <a href="/login/twitter" class="btn btn-twitter">Authorize Twitter to Post</a>
            {% else %}
                <button type="submit" class="btn btn-twitter">Post to Twitter</button>
                <div class="status">Connected as: {{ username }}</div>
            {% endif %}
        </form>
        
        {% if message %}
            <div class="status">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    message = request.args.get('message')
    logged_in = 'twitter_token' in session
    username = session.get('twitter_user', '')
    return render_template_string(LAYOUT_TEMPLATE, logged_in=logged_in, username=username, message=message)

@app.route('/login/twitter')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = oauth.twitter.authorize_access_token()
    # In a real app, you'd store this token in a database associated with the user
    session['twitter_token'] = token
    
    resp = oauth.twitter.get('account/verify_credentials.json')
    session['twitter_user'] = resp.json().get('screen_name')
    
    return redirect(url_for('index'))

@app.route('/share', method=['POST'])
def share_content():
    if 'twitter_token' not in session:
        return redirect(url_for('login'))
    
    content = request.form.get('content')
    
    # Payload formatting for the specific API (Twitter v1.1 example)
    payload = {'status': content}
    
    try:
        # Posting content on behalf of the user using their access token
        response = oauth.twitter.post('statuses/update.json', data=payload)
        response.raise_for_status()
        message = "Successfully shared to Twitter!"
    except Exception as e:
        message = f"Error sharing: {str(e)}"
    
    return redirect(url_for('index', message=message))

if __name__ == '__main__':
    # Required: pip install Flask Authlib requests
    app.run(debug=True, port=5000)