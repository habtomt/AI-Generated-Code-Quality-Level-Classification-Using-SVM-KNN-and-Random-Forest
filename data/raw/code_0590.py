"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_004.txt
Run      : 1
"""

from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, body):
    """Send SMS message to a specified phone number with the given message body."""
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_NUMBER,
            to=to
        )
        return message.sid
    except Exception as e:
        return str(e)

@app.route('/send_update', methods=['POST'])
def send_update():
    """
    Endpoint to send SMS updates.
    Expect a JSON payload with 'to' (customer's phone number) and 'status'
    (order status message).
    """
    data = request.json

    phone_number = data.get("to")
    order_status = data.get("status")

    if not phone_number or not order_status:
        return jsonify({"error": "Missing 'to' or 'status' fields"}), 400

    try:
        # Send the SMS
        message_sid = send_sms(phone_number, order_status)
        return jsonify({"status": "SMS sent", "message_sid": message_sid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run the application
    app.run(debug=True)