"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_003.txt
Run      : 3
"""

# Import the required libraries
import os
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Set the database connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webhook_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the database model for storing webhook data
class WebhookData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Text, nullable=False)

# Define the endpoint for receiving webhooks
@app.route('/webhook', methods=['POST'])
def receive_webhook():
    try:
        # Get the payload from the request
        payload = request.get_json()
        
        # Store the payload in the database
        webhook_data = WebhookData(payload=json.dumps(payload))
        db.session.add(webhook_data)
        db.session.commit()
        
        # Return a success response
        return 'Webhook received and stored successfully'
    except Exception as e:
        # Handle any errors that occur
        db.session.rollback()
        return str(e), 500

# Run the application
if __name__ == '__main__':
    db.create_all()  # Create the database tables
    app.run(debug=True, port=5000)