"""
Auto-generated Python code
Scenario : Cloud Hosting
Prompt   : response_003.txt
Run      : 3
"""

# Import the required libraries
import os
from flask import Flask, request, send_from_directory
from flask_caching import Cache

# Initialize the Flask app
app = Flask(__name__)

# Initialize the cache with a Redis backend (you'll need to install redis-py and redis)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app)

# Initialize the cache with a default expiration time (you can adjust this as needed)
cache.init_app(app, config={'CACHE_DEFAULT_TIMEOUT': 60})  # 1 minute default timeout

# Define a helper function to serve static assets from a directory
def serve_static(directory, filename):
    # Try to serve the file from the cache first
    try:
        result = cache.get(filename)
        if result:
            return result
    except Exception as e:
        print(f"Error serving from cache: {e}")

    # If not found in cache, try to serve from disk
    try:
        return send_from_directory(directory, filename)
    except Exception as e:
        print(f"Error serving from disk: {e}")

# Define a route for serving static assets
@app.route('/static/<path:path>')
def serve_static_asset(path):
    # Use the helper function to serve the static asset
    return serve_static('/path/to/static/assets', path)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)