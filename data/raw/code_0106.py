from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Mock storage for user access tokens
USER_TOKENS = {
    "facebook": os.getenv("FACEBOOK_TOKEN", "mock_facebook_token"),
    "twitter": os.getenv("TWITTER_TOKEN", "mock_twitter_token"),
}

FACEBOOK_POST_URL = "https://graph.facebook.com/v19.0/me/feed"
TWITTER_POST_URL = "https://api.twitter.com/2/tweets"


def format_content(content, platform):
    if platform == "twitter":
        return content[:280]
    return content


def post_to_facebook(content, token):
    payload = {
        "message": content,
        "access_token": token
    }
    # Mock request (would be real in production)
    return {"status": "posted_to_facebook", "payload": payload}


def post_to_twitter(content, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": content
    }
    # Mock request (would be real in production)
    return {"status": "posted_to_twitter", "payload": payload}


@app.route("/share/facebook", methods=["POST"])
def share_facebook():
    data = request.json
    content = data.get("content", "")
    content = format_content(content, "facebook")

    token = USER_TOKENS["facebook"]

    result = post_to_facebook(content, token)
    return jsonify(result)


@app.route("/share/twitter", methods=["POST"])
def share_twitter():
    data = request.json
    content = data.get("content", "")
    content = format_content(content, "twitter")

    token = USER_TOKENS["twitter"]

    result = post_to_twitter(content, token)
    return jsonify(result)


@app.route("/permissions")
def permissions():
    return jsonify({
        "facebook": "read_write",
        "twitter": "tweet.write"
    })


@app.route("/craft", methods=["POST"])
def craft_content():
    data = request.json
    base = data.get("text", "")
    tags = data.get("tags", [])

    formatted = base
    if tags:
        formatted += "\n\n" + " ".join(f"#{t}" for t in tags)

    return jsonify({
        "original": base,
        "formatted": formatted
    })


if __name__ == "__main__":
    app.run(debug=True)