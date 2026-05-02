# telemedicine_system.py

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_socketio import SocketIO, join_room, emit
import os
import uuid
import hashlib
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "super_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage
users = {}
sessions = {}
appointments = []
medical_records = {}

UPLOAD_FOLDER = "records"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------- AUTH -----------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = hash_password(data["password"])
    role = data.get("role", "patient")

    if username in users:
        return jsonify({"error": "User exists"}), 400

    users[username] = {"password": password, "role": role}
    return jsonify({"message": "Registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = hash_password(data["password"])

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = str(uuid.uuid4())
    sessions[token] = username
    return jsonify({"token": token})

def auth(token):
    return sessions.get(token)

# ----------------- APPOINTMENTS -----------------

@app.route("/appointment", methods=["POST"])
def create_appointment():
    token = request.headers.get("Authorization")
    user = auth(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    appointment = {
        "id": str(uuid.uuid4()),
        "patient": user,
        "doctor": data["doctor"],
        "time": data["time"],
        "created_at": str(datetime.datetime.now())
    }
    appointments.append(appointment)
    return jsonify(appointment)

@app.route("/appointments", methods=["GET"])
def list_appointments():
    return jsonify(appointments)

# ----------------- MEDICAL RECORDS -----------------

@app.route("/upload_record", methods=["POST"])
def upload_record():
    token = request.headers.get("Authorization")
    user = auth(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files["file"]
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    medical_records.setdefault(user, []).append(filename)
    return jsonify({"message": "Uploaded", "file": filename})

@app.route("/records", methods=["GET"])
def list_records():
    token = request.headers.get("Authorization")
    user = auth(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(medical_records.get(user, []))

@app.route("/records/<filename>")
def get_record(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ----------------- VIDEO CALL (WebRTC SIGNALING) -----------------

rooms = {}

@app.route("/call/<room>")
def call_page(room):
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Telemedicine Call</title>
</head>
<body>
    <h2>Secure Video Call Room: {{room}}</h2>
    <video id="localVideo" autoplay muted></video>
    <video id="remoteVideo" autoplay></video>

    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <script>
        const socket = io();
        const room = "{{room}}";

        let localStream;
        let peerConnection;

        const config = { iceServers: [{ urls: "stun:stun.l.google.com:19302" }] };

        async function start() {
            localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            document.getElementById("localVideo").srcObject = localStream;

            peerConnection = new RTCPeerConnection(config);

            localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

            peerConnection.ontrack = (event) => {
                document.getElementById("remoteVideo").srcObject = event.streams[0];
            };

            peerConnection.onicecandidate = (event) => {
                if (event.candidate) {
                    socket.emit("signal", { room, data: event.candidate });
                }
            };

            socket.emit("join", room);
        }

        socket.on("signal", async (data) => {
            if (data.offer) {
                await peerConnection.setRemoteDescription(data.offer);
                const answer = await peerConnection.createAnswer();
                await peerConnection.setLocalDescription(answer);
                socket.emit("signal", { room, data: { answer } });
            }

            if (data.answer) {
                await peerConnection.setRemoteDescription(data.answer);
            }

            if (data.candidate) {
                await peerConnection.addIceCandidate(data.candidate);
            }
        });

        async function createOffer() {
            const offer = await peerConnection.createOffer();
            await peerConnection.setLocalDescription(offer);
            socket.emit("signal", { room, data: { offer } });
        }

        socket.on("connect", start);
        setTimeout(createOffer, 2000);
    </script>
</body>
</html>
""", room=room)

@socketio.on("join")
def on_join(room):
    join_room(room)
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(request.sid)

@socketio.on("signal")
def signal(data):
    room = data["room"]
    emit("signal", data["data"], room=room, include_self=False)

# ----------------- RUN -----------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)