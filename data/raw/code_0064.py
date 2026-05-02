#!/usr/bin/env python3

from flask import Flask, request, jsonify
import time
import threading
import math
import random

app = Flask(__name__)

users = {}


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def init_user(user_id, lat, lon):
    users[user_id] = {
        "path": [(lat, lon, time.time())],
        "total_distance": 0.0,
        "last_update": time.time(),
        "active": True
    }


@app.route("/start", methods=["POST"])
def start():
    data = request.json
    user_id = data["user_id"]
    lat = data["lat"]
    lon = data["lon"]

    init_user(user_id, lat, lon)
    return jsonify({"status": "started", "user_id": user_id})


@app.route("/update", methods=["POST"])
def update():
    data = request.json
    user_id = data["user_id"]
    lat = data["lat"]
    lon = data["lon"]
    t = time.time()

    if user_id not in users:
        return jsonify({"error": "user not found"}), 404

    user = users[user_id]
    last_lat, last_lon, last_t = user["path"][-1]

    dist = haversine(last_lat, last_lon, lat, lon)
    user["total_distance"] += dist
    user["path"].append((lat, lon, t))
    user["last_update"] = t

    return jsonify({"distance_added_km": dist})


@app.route("/summary/<user_id>", methods=["GET"])
def summary(user_id):
    if user_id not in users:
        return jsonify({"error": "user not found"}), 404

    user = users[user_id]
    path = user["path"]

    total_time = path[-1][2] - path[0][2] if len(path) > 1 else 0.0
    speed = (user["total_distance"] / (total_time / 3600)) if total_time > 0 else 0.0

    return jsonify({
        "total_distance_km": user["total_distance"],
        "total_time_sec": total_time,
        "avg_speed_kmh": speed,
        "points": len(path)
    })


def simulate_movement(user_id):
    while True:
        if user_id in users:
            last_lat, last_lon, _ = users[user_id]["path"][-1]

            new_lat = last_lat + random.uniform(-0.001, 0.001)
            new_lon = last_lon + random.uniform(-0.001, 0.001)

            users[user_id]["path"].append((new_lat, new_lon, time.time()))
            time.sleep(2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)