from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "webhooks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS webhook_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            payload TEXT,
            received_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_event(event_type, payload):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO webhook_events (event_type, payload, received_at)
        VALUES (?, ?, ?)
    """, (event_type, str(payload), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

@app.route("/webhook", methods=["POST"])
def webhook_listener():
    try:
        data = request.get_json(force=True)

        event_type = data.get("event_type", "unknown")
        payload = data.get("data", data)

        save_event(event_type, payload)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)