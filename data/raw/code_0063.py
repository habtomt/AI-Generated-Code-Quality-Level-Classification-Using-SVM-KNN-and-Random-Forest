#!/usr/bin/env python3

from flask import Flask, request, jsonify
import math
import threading
import time

app = Flask(__name__)

responders = {}
incidents = []


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_nearest_responder(lat, lon):
    best_id = None
    best_dist = float("inf")

    for rid, data in responders.items():
        dist = haversine(lat, lon, data["lat"], data["lon"])
        if dist < best_dist:
            best_dist = dist
            best_id = rid

    return best_id, best_dist


@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json
    responder_id = data["responder_id"]
    lat = data["lat"]
    lon = data["lon"]

    responders[responder_id] = {
        "lat": lat,
        "lon": lon,
        "timestamp": time.time()
    }

    return jsonify({"status": "updated"})


@app.route("/incident", methods=["POST"])
def incident():
    data = request.json
    lat = data["lat"]
    lon = data["lon"]
    severity = data.get("severity", 1)

    responder_id, distance = find_nearest_responder(lat, lon)

    incident = {
        "lat": lat,
        "lon": lon,
        "severity": severity,
        "assigned_responder": responder_id,
        "distance_km": distance,
        "timestamp": time.time()
    }

    incidents.append(incident)

    return jsonify(incident)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "responders": responders,
        "incidents": incidents
    })


def cleanup_loop():
    while True:
        now = time.time()
        expired = [r for r, d in responders.items() if now - d["timestamp"] > 60]
        for r in expired:
            del responders[r]
        time.sleep(10)


if __name__ == "__main__":
    t = threading.Thread(target=cleanup_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=False)