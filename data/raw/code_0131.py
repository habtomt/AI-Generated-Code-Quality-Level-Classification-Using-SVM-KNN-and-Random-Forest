#!/usr/bin/env python3
import os
import uuid
import sqlite3
from flask import Flask, request, jsonify, send_from_directory, session

APP = Flask(__name__)
APP.secret_key = "supersecretkey"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "app.db")

os.makedirs(UPLOAD_DIR, exist_ok=True)


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id TEXT PRIMARY KEY,
        bio TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        title TEXT,
        filename TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return user


def require_login():
    return current_user() is not None


@APP.route("/register", methods=["POST"])
def register():
    data = request.json
    uid = str(uuid.uuid4())

    conn = db()
    conn.execute(
        "INSERT INTO users VALUES (?,?,?,?)",
        (uid, data["username"], data["password"], "user"),
    )
    conn.execute(
        "INSERT INTO profiles VALUES (?,?)",
        (uid, "")
    )
    conn.commit()
    conn.close()

    return jsonify({"user_id": uid})


@APP.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "invalid"}), 401

    session["user_id"] = user["id"]
    return jsonify({"message": "logged in"})


@APP.route("/profile", methods=["GET", "POST"])
def profile():
    if not require_login():
        return jsonify({"error": "login required"}), 401

    user = current_user()
    conn = db()

    if request.method == "POST":
        bio = request.json.get("bio", "")
        conn.execute(
            "UPDATE profiles SET bio=? WHERE user_id=?",
            (bio, user["id"])
        )
        conn.commit()

    profile = conn.execute(
        "SELECT * FROM profiles WHERE user_id=?",
        (user["id"],)
    ).fetchone()

    conn.close()

    return jsonify({"username": user["username"], "bio": profile["bio"]})


@APP.route("/upload", methods=["POST"])
def upload():
    if not require_login():
        return jsonify({"error": "login required"}), 401

    file = request.files["file"]
    title = request.form.get("title", "untitled")

    vid = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, vid + "_" + file.filename)
    file.save(path)

    conn = db()
    conn.execute(
        "INSERT INTO videos VALUES (?,?,?,?,?)",
        (vid, current_user()["id"], title, path, "pending")
    )
    conn.commit()
    conn.close()

    return jsonify({"video_id": vid})


@APP.route("/moderate/<video_id>/<action>", methods=["POST"])
def moderate(video_id, action):
    user = current_user()
    if not user or user["role"] != "admin":
        return jsonify({"error": "admin only"}), 403

    status = "approved" if action == "approve" else "rejected"

    conn = db()
    conn.execute(
        "UPDATE videos SET status=? WHERE id=?",
        (status, video_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": status})


@APP.route("/videos")
def list_videos():
    conn = db()
    videos = conn.execute(
        "SELECT * FROM videos WHERE status='approved'"
    ).fetchall()
    conn.close()

    return jsonify([dict(v) for v in videos])


@APP.route("/pending")
def pending():
    user = current_user()
    if not user or user["role"] != "admin":
        return jsonify({"error": "admin only"}), 403

    conn = db()
    videos = conn.execute(
        "SELECT * FROM videos WHERE status='pending'"
    ).fetchall()
    conn.close()

    return jsonify([dict(v) for v in videos])


@APP.route("/video/<video_id>")
def get_video(video_id):
    conn = db()
    video = conn.execute(
        "SELECT * FROM videos WHERE id=?",
        (video_id,)
    ).fetchone()
    conn.close()

    if not video or video["status"] != "approved":
        return jsonify({"error": "not available"}), 404

    return send_from_directory("/", video["filename"])


@APP.route("/init_admin")
def init_admin():
    conn = db()
    uid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO users VALUES (?,?,?,?)",
        (uid, "admin", "admin", "admin")
    )
    conn.execute(
        "INSERT INTO profiles VALUES (?,?)",
        (uid, "admin")
    )
    conn.commit()
    conn.close()

    return jsonify({"admin_user": "admin/admin"})


if __name__ == "__main__":
    init_db()
    APP.run(debug=True, host="0.0.0.0", port=5000)