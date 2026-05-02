from flask import Flask, render_template_string
import random
from datetime import datetime, timedelta

app = Flask(__name__)


def generate_mock_data():
    days = 30
    base_date = datetime.now()

    data = []
    followers = 1000

    for i in range(days):
        date = (base_date - timedelta(days=days - i)).strftime("%Y-%m-%d")
        engagement = random.randint(50, 300)
        growth = random.randint(-20, 100)
        followers += growth

        data.append({
            "date": date,
            "engagement": engagement,
            "followers": followers,
            "posts": random.randint(1, 10),
            "likes": random.randint(20, 500),
            "comments": random.randint(5, 100),
        })

    return data


@app.route("/")
def dashboard():
    data = generate_mock_data()

    dates = [d["date"] for d in data]
    engagement = [d["engagement"] for d in data]
    followers = [d["followers"] for d in data]
    likes = [d["likes"] for d in data]

    html = """
    <html>
    <head>
        <title>Social Media Analytics Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>Social Media Analytics Dashboard</h1>

        <div id="engagement" style="width:100%;height:400px;"></div>
        <div id="followers" style="width:100%;height:400px;"></div>
        <div id="likes" style="width:100%;height:400px;"></div>

        <script>
            var dates = {{ dates|safe }};
            var engagement = {{ engagement|safe }};
            var followers = {{ followers|safe }};
            var likes = {{ likes|safe }};

            Plotly.newPlot("engagement", [{
                x: dates,
                y: engagement,
                type: "scatter",
                name: "Engagement"
            }], {title: "User Engagement"});

            Plotly.newPlot("followers", [{
                x: dates,
                y: followers,
                type: "scatter",
                name: "Followers"
            }], {title: "Follower Growth"});

            Plotly.newPlot("likes", [{
                x: dates,
                y: likes,
                type: "scatter",
                name: "Likes"
            }], {title: "Post Performance (Likes)"});
        </script>
    </body>
    </html>
    """

    return render_template_string(
        html,
        dates=dates,
        engagement=engagement,
        followers=followers,
        likes=likes
    )


if __name__ == "__main__":
    app.run(debug=True)