"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_002.txt
Run      : 1
"""

# Importing necessary libraries
from flask import Flask, request, jsonify
from twilio.rest import Client
import sqlite3
import schedule
import time
import logging

# Create a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = 'YOUR_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_NUMBER'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Database setup (SQLite for simplicity)
def init_db():
    try:
        con = sqlite3.connect('subscribers.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS subscribers
                       (id INTEGER PRIMARY KEY, phone_number TEXT)''')
        con.commit()
        con.close()
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")

def schedule_message(message):
    try:
        schedule.every(1).day.at("10:00").do(send_message, message)
    except Exception as e:
        logger.error(f"Error scheduling message: {e}")

def send_message(message):
    try:
        con = sqlite3.connect('subscribers.db')
        cur = con.cursor()
        cur.execute("SELECT phone_number FROM subscribers")
        subscribers = cur.fetchall()
        for subscriber in subscribers:
            phone_number = subscriber[0]
            client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
        con.close()
        logger.info(f"Messages sent successfully!")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        phone_number = request.json.get('phone_number')
        if not phone_number:
            return jsonify({"message": "Invalid phone number"}), 400

        con = sqlite3.connect('subscribers.db')
        cur = con.cursor()
        cur.execute("INSERT INTO subscribers (phone_number) VALUES (?)", (phone_number,))
        con.commit()
        con.close()
        logger.info(f"Subscribed {phone_number} successfully!")
        return jsonify({"message": "Subscribed successfully!"}), 200
    except Exception as e:
        logger.error(f"Error subscribing user: {e}")
        return jsonify({"message": "Error subscribing user"}), 500

@app.route('/send_message', methods=['POST'])
def schedule_message_endpoint():
    try:
        message = request.json.get('message')
        if not message:
            return jsonify({"message": "Invalid message"}), 400

        schedule_message(message)
        logger.info(f"Message scheduled: {message}")
        return jsonify({"message": "Message scheduled successfully!"}), 200
    except Exception as e:
        logger.error(f"Error scheduling message: {e}")
        return jsonify({"message": "Error scheduling message"}), 500

if __name__ == '__main__':
    init_db()
    schedule.every(1).day.at("10:00").do(send_message, "Test message")
    while True:
        schedule.run_pending()
        time.sleep(1)
    app.run(debug=True)