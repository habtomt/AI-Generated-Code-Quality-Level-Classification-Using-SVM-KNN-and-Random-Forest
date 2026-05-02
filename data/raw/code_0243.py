import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect('webhooks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webhook_payloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_event TEXT,
            payload_data TEXT,
            received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- Webhook Listener Endpoint ---
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Endpoint to receive, parse, and store incoming webhook data.
    """
    # Check if the payload is valid JSON
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400

    payload = request.get_json()

    # Parse relevant data (Example: extracting 'event_type' and the full body)
    event_type = payload.get('event', 'unknown_event')
    
    try:
        # Store in database
        conn = sqlite3.connect('webhooks.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO webhook_payloads (source_event, payload_data) VALUES (?, ?)",
            (event_type, str(payload))
        )
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Data stored"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    # Listen on all interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)