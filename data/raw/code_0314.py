"""
Auto-generated Python code
Scenario : Blockchain & Cryptocurrency
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from blockchain import Blockchain

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.balance = 0.0

# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

# Define a function to create a new blockchain
def create_blockchain():
    return Blockchain()

# Initialize the blockchain
blockchain = create_blockchain()

# Define a route to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data['username'] and data['password']:
        try:
            # Create a new user
            user = User(data['username'], data['password'])
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid request'}), 400

# Define a route to login a user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] and data['password']:
        try:
            # Get the user
            user = User.query.filter_by(username=data['username']).first()
            if user and check_password_hash(user.password, data['password']):
                return jsonify({'message': 'Login successful'}), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid request'}), 400

# Define a route to make a transaction
@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.get_json()
    if data['sender'] and data['receiver'] and data['amount']:
        try:
            # Get the sender and receiver
            sender = User.query.filter_by(username=data['sender']).first()
            receiver = User.query.filter_by(username=data['receiver']).first()
            if sender and receiver:
                # Create a new transaction
                transaction = Transaction(sender_id=sender.id, receiver_id=receiver.id, amount=data['amount'])
                db.session.add(transaction)
                db.session.commit()
                # Add the transaction to the blockchain
                blockchain.add_transaction(transaction)
                return jsonify({'message': 'Transaction created successfully'}), 201
            else:
                return jsonify({'message': 'Invalid sender or receiver'}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid request'}), 400

# Define a route to get the blockchain
@app.route('/blockchain', methods=['GET'])
def blockchain():
    return jsonify(blockchain.get_chain()), 200

# Run the app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)