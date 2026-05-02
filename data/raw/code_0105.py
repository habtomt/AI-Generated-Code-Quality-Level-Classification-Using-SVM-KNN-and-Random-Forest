from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

SOCIAL_API_URL = "https://jsonplaceholder.typicode.com/posts"
IMAGE_API_URL = "https://jsonplaceholder.typicode.com/photos?_limit=10"


def fetch_posts():
    posts = requests.get(SOCIAL_API_URL).json()[:10]
    images = requests.get(IMAGE_API_URL).json()

    feed = []

    for i, post in enumerate(posts):
        feed.append({
            "type": "text",
            "title": post["title"],
            "content": post["body"]
        })

    for img in images:
        feed.append({
            "type": "image",
            "title": img["title"],
            "url": img["url"]
        })

    return feed


@app.route("/api/feed")
def api_feed():
    return jsonify(fetch_posts())


@app.route("/feed")
def feed_page():
    feed = fetch_posts()

    html = """
    <h1>Social Media Feed</h1>
    {% for item in feed %}
        <div style="margin-bottom:20px;">
            {% if item.type == 'text' %}
                <h3>{{ item.title }}</h3>
                <p>{{ item.content }}</p>
            {% elif item.type == 'image' %}
                <h3>{{ item.title }}</h3>
                <img src="{{ item.url }}" width="300"/>
            {% endif %}
        </div>
    {% endfor %}
    """

    return render_template_string(html, feed=feed)


if __name__ == "__main__":
    app.run(debug=True)