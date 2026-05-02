#!/usr/bin/env python3
import os
import json
from flask import Flask, request, jsonify, render_template_string

APP = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "interactive_video.json")

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)


@APP.route("/create_video", methods=["POST"])
def create_video():
    data = request.json
    video_id = data["video_id"]

    db = load_db()
    db[video_id] = {
        "video_url": data["video_url"],
        "quiz": data.get("quiz", []),
        "annotations": data.get("annotations", []),
        "links": data.get("links", [])
    }
    save_db(db)

    return jsonify({"status": "created", "video_id": video_id})


@APP.route("/video/<video_id>")
def video_page(video_id):
    db = load_db()
    video = db.get(video_id)

    if not video:
        return "Video not found", 404

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Video</title>
        <style>
            #container { position: relative; width: 800px; margin: auto; }
            #video { width: 100%; }
            .overlay {
                position: absolute;
                top: 10px;
                left: 10px;
                background: rgba(0,0,0,0.6);
                color: white;
                padding: 10px;
                display: none;
            }
            #quizBox {
                position: absolute;
                bottom: 20px;
                left: 20px;
                background: white;
                padding: 10px;
                display: none;
            }
        </style>
    </head>
    <body>

    <div id="container">
        <video id="video" controls>
            <source src="{{video_url}}" type="video/mp4">
        </video>

        <div id="annotation" class="overlay"></div>

        <div id="quizBox">
            <p id="question"></p>
            <button onclick="answer(true)">True</button>
            <button onclick="answer(false)">False</button>
        </div>
    </div>

    <script>
        const quiz = {{quiz | safe}};
        const annotations = {{annotations | safe}};
        const links = {{links | safe}};

        const video = document.getElementById("video");
        const annotationBox = document.getElementById("annotation");
        const quizBox = document.getElementById("quizBox");
        const questionEl = document.getElementById("question");

        let quizIndex = 0;
        let annotationIndex = 0;

        video.addEventListener("timeupdate", () => {
            let t = video.currentTime;

            if (annotationIndex < annotations.length) {
                let a = annotations[annotationIndex];
                if (t >= a.time) {
                    annotationBox.style.display = "block";
                    annotationBox.innerHTML = a.text;
                    setTimeout(() => annotationBox.style.display = "none", 4000);
                    annotationIndex++;
                }
            }

            if (quizIndex < quiz.length) {
                let q = quiz[quizIndex];
                if (t >= q.time) {
                    video.pause();
                    quizBox.style.display = "block";
                    questionEl.innerText = q.question;
                }
            }
        });

        function answer(val) {
            quizBox.style.display = "none";
            quizIndex++;
            video.play();
        }

        links.forEach(l => {
            let btn = document.createElement("button");
            btn.innerText = l.label;
            btn.style.position = "absolute";
            btn.style.bottom = "10px";
            btn.style.right = "10px";
            btn.onclick = () => window.open(l.url, "_blank");
            document.getElementById("container").appendChild(btn);
        });
    </script>

    </body>
    </html>
    """

    return render_template_string(
        html,
        video_url=video["video_url"],
        quiz=json.dumps(video["quiz"]),
        annotations=json.dumps(video["annotations"]),
        links=json.dumps(video["links"])
    )


@APP.route("/add_interaction/<video_id>", methods=["POST"])
def add_interaction(video_id):
    data = request.json
    db = load_db()

    if video_id not in db:
        return jsonify({"error": "not found"}), 404

    db[video_id].setdefault("quiz", []).extend(data.get("quiz", []))
    db[video_id].setdefault("annotations", []).extend(data.get("annotations", []))
    db[video_id].setdefault("links", []).extend(data.get("links", []))

    save_db(db)
    return jsonify({"status": "updated"})


if __name__ == "__main__":
    APP.run(debug=True, host="0.0.0.0", port=5050)