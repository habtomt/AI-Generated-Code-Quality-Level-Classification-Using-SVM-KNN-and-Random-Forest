#!/usr/bin/env python3
import os
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

APP = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "analytics.db")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        title TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS views (
        id TEXT PRIMARY KEY,
        video_id TEXT,
        timestamp TEXT,
        watch_time INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS engagement (
        id TEXT PRIMARY KEY,
        video_id TEXT,
        likes INTEGER,
        comments INTEGER,
        shares INTEGER
    )
    """)

    conn.commit()
    conn.close()


@APP.route("/add_video", methods=["POST"])
def add_video():
    data = request.json
    vid = str(uuid.uuid4())

    conn = db()
    conn.execute(
        "INSERT INTO videos VALUES (?,?)",
        (vid, data.get("title", "untitled"))
    )
    conn.commit()
    conn.close()

    return jsonify({"video_id": vid})


@APP.route("/simulate_view", methods=["POST"])
def simulate_view():
    data = request.json
    conn = db()

    conn.execute(
        "INSERT INTO views VALUES (?,?,?,?)",
        (
            str(uuid.uuid4()),
            data["video_id"],
            datetime.utcnow().isoformat(),
            data.get("watch_time", 30)
        )
    )

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@APP.route("/simulate_engagement", methods=["POST"])
def simulate_engagement():
    data = request.json
    conn = db()

    conn.execute(
        "INSERT INTO engagement VALUES (?,?,?,?,?)",
        (
            str(uuid.uuid4()),
            data["video_id"],
            data.get("likes", 0),
            data.get("comments", 0),
            data.get("shares", 0),
        )
    )

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


def get_metrics(video_id):
    conn = db()

    views = conn.execute(
        "SELECT COUNT(*) as c, AVG(watch_time) as avg_watch FROM views WHERE video_id=?",
        (video_id,)
    ).fetchone()

    eng = conn.execute(
        "SELECT SUM(likes) as likes, SUM(comments) as comments, SUM(shares) as shares FROM engagement WHERE video_id=?",
        (video_id,)
    ).fetchone()

    conn.close()

    return {
        "views": views["c"] or 0,
        "avg_watch": views["avg_watch"] or 0,
        "likes": eng["likes"] or 0,
        "comments": eng["comments"] or 0,
        "shares": eng["shares"] or 0,
    }


@APP.route("/dashboard/<video_id>")
def dashboard(video_id):
    metrics = get_metrics(video_id)

    html = """
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h2>Video Analytics Dashboard</h2>

        <div id="chart"></div>

        <script>
            var data = [{
                x: ["Views", "Likes", "Comments", "Shares"],
                y: [{{v}}, {{l}}, {{c}}, {{s}}],
                type: "bar"
            }];

            Plotly.newPlot('chart', data);
        </script>

        <h3>Metrics</h3>
        <p>Views: {{v}}</p>
        <p>Avg Watch Time: {{a}}</p>
        <p>Likes: {{l}}</p>
        <p>Comments: {{c}}</p>
        <p>Shares: {{s}}</p>
    </body>
    </html>
    """

    return render_template_string(
        html,
        v=metrics["views"],
        l=metrics["likes"],
        c=metrics["comments"],
        s=metrics["shares"],
        a=metrics["avg_watch"]
    )


@APP.route("/report/<video_id>")
def report(video_id):
    metrics = get_metrics(video_id)

    retention = min(100, metrics["avg_watch"] * 2)

    return jsonify({
        "video_id": video_id,
        "views": metrics["views"],
        "engagement": {
            "likes": metrics["likes"],
            "comments": metrics["comments"],
            "shares": metrics["shares"]
        },
        "retention_rate": retention
    })


@APP.route("/custom_report", methods=["POST"])
def custom_report():
    data = request.json
    video_ids = data.get("video_ids", [])

    results = []
    for vid in video_ids:
        results.append(get_metrics(vid))

    return jsonify({"report": results})


if __name__ == "__main__":
    init_db()
    APP.run(debug=True, host="0.0.0.0", port=5001)