"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_003.txt
Run      : 2
"""

# Import required libraries
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import logging

# Create a Flask application
app = Flask(__name__)

# Set up database connection using Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webhook_data.db'
db = SQLAlchemy(app)

# Define the database model for storing webhook data
class WebhookData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Text, nullable=False)

# Define the webhook endpoint
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Get the webhook payload from the request body
        payload = request.get_json()
        
        # Log the incoming webhook request
        logging.info(f'Received webhook payload: {json.dumps(payload)}')
        
        # Create a new database entry for the webhook data
        webhook_data = WebhookData(payload=json.dumps(payload))
        db.session.add(webhook_data)
        db.session.commit()
        
        # Return a success response to the webhook sender
        return 'Webhook received successfully', 200
    
    except Exception as e:
        # Log any errors that occur during webhook processing
        logging.error(f'Error handling webhook: {str(e)}')
        return 'Error handling webhook', 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)