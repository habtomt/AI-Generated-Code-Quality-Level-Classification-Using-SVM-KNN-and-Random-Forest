"""
Auto-generated Python code
Scenario : Serverless Deployment
Prompt   : response_003.txt
Run      : 1
"""

# Import necessary packages
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask application and specify SQLite as the database
app = Flask(__name__)
# Specify the path to the SQLite database file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'webhooks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a model for the database
class WebhookData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.String, nullable=False)

# Create the tables
with app.app_context():
    db.create_all()

# Define a function to handle incoming webhooks
def handle_webhook(data):
    try:
        # Extract relevant fields from the payload (you may need to adjust this
        # based on the structure of the incoming payload)
        relevant_data = data.get('relevant_field', 'default_value')

        # Store the relevant data in the database
        new_entry = WebhookData(payload=str(relevant_data))
        db.session.add(new_entry)
        db.session.commit()

        # Respond with a success message
        return {'message': 'Data received and stored'}, 200

    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred', 'message': str(e)}, 500

# Define a route to handle incoming webhooks
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get JSON payload from the incoming request
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data received'}), 400

    return handle_webhook(data)

# Run the application
if __name__ == '__main__':
    app.run(port=5000, debug=True)