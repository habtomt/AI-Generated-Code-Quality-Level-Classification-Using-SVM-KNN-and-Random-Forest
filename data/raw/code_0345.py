"""
Auto-generated Python code
Scenario : Cloud Hosting
Prompt   : response_003.txt
Run      : 2
"""

import os
import redis
from flask import Flask, send_from_directory

# Initialize Flask app
app = Flask(__name__)

# Initialize Redis cache
redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Replace with your Redis instance

# Define cache key prefix
CACHE_KEY_PREFIX = 'static_assets_'

# Define cache expiration time (in seconds)
CACHE_EXPIRATION_TIME = 3600  # 1 hour

# Define static assets directory
STATIC_ASSETS_DIR = 'assets'

# Route for serving static assets
@app.route('/<path:path>')
def serve_static_asset(path):
    try:
        # Generate cache key
        cache_key = f'{CACHE_KEY_PREFIX}{path}'

        # Check if asset is cached
        cached_asset = redis_client.get(cache_key)

        # If asset is cached, return it
        if cached_asset:
            return cached_asset

        # If asset is not cached, fetch it and cache it
        asset_path = os.path.join(STATIC_ASSETS_DIR, path)
        with open(asset_path, 'rb') as file:
            asset_data = file.read()

        # Cache asset
        redis_client.set(cache_key, asset_data)
        redis_client.expire(cache_key, CACHE_EXPIRATION_TIME)

        # Return asset
        return asset_data

    except Exception as e:
        # Log exception
        print(f'Error serving static asset: {e}')

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)