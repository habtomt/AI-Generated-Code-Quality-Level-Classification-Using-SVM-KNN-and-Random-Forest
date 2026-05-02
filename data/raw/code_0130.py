#!/usr/bin/env python3
import os
import uuid
import json
import subprocess
from flask import Flask, request, jsonify, send_from_directory, render_template_string

APP = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "videos")
DB_FILE = os.path.join(BASE_DIR, "db.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)


def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)


def run(cmd):
    subprocess.run(cmd, check=True)


def transcode_hls(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    renditions = [
        ("1080p", "1920x1080", "5000k"),
        ("720p", "1280x720", "2800k"),
        ("480p", "854x480", "1400k"),
    ]

    playlists = []

    for name, res, br in renditions:
        out_path = os.path.join(output_dir, name)
        os.makedirs(out_path, exist_ok=True)

        playlist = os.path.join(out_path, "index.m3u8")

        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vf", f"scale={res}",
            "-c:v", "libx264",
            "-b:v", br,
            "-c:a", "aac",
            "-hls_time", "4",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", f"{out_path}/seg_%03d.ts",
            playlist,
        ]

        run(cmd)
        playlists.append((name, playlist))

    master_path = os.path.join(output_dir, "master.m3u8")
    with open(master_path, "w") as f:
        f.write("#EXTM3U\n")
        for name, _ in playlists:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH=8000000\n{name}/index.m3u8\n")

    return master_path


@APP.route("/")
def index():
    db = load_db()
    return jsonify(db)


@APP.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    category = request.form.get("category", "default")

    video_id = str(uuid.uuid4())
    category_dir = os.path.join(UPLOAD_DIR, category)
    video_dir = os.path.join(category_dir, video_id)
    os.makedirs(video_dir, exist_ok=True)

    input_path = os.path.join(video_dir, file.filename)
    file.save(input_path)

    output_dir = os.path.join(video_dir, "hls")
    master_playlist = transcode_hls(input_path, output_dir)

    db = load_db()
    db[video_id] = {
        "category": category,
        "path": video_dir,
        "master": master_playlist
    }
    save_db(db)

    return jsonify({"video_id": video_id})


@APP.route("/videos/<video_id>")
def play(video_id):
    db = load_db()
    video = db.get(video_id)
    if not video:
        return "Not found", 404

    master = video["master"]
    rel_dir = os.path.dirname(master)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    </head>
    <body>
        <video id="video" controls style="width:80%"></video>
        <script>
            var video = document.getElementById('video');
            var videoSrc = "/hls/{{path}}/master.m3u8";

            if (Hls.isSupported()) {
                var hls = new Hls();
                hls.loadSource(videoSrc);
                hls.attachMedia(video);
            } else {
                video.src = videoSrc;
            }
        </script>
    </body>
    </html>
    """

    rel_path = os.path.relpath(master, BASE_DIR).replace("\\", "/")
    return render_template_string(html, path=rel_path)


@APP.route("/hls/<path:filename>")
def hls(filename):
    return send_from_directory(BASE_DIR, filename)


@APP.route("/list")
def list_videos():
    return jsonify(load_db())


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000, debug=True)