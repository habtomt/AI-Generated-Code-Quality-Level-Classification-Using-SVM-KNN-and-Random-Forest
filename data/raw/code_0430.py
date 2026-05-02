"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_003.txt
Run      : 1
"""

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# Create a new Flask application
app = Flask(__name__)

# Set up JWT configuration
app.config['JWT_SECRET_KEY'] = 'YOUR_SECRET_KEY'  # Replace with your own secret key
jwt = JWTManager(app)

# Set up Bcrypt configuration
bcrypt = Bcrypt(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['userAuth']
users_collection = db['users']

# Define a function to hash a password
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Define a function to compare a password with a hashed password
def compare_password(password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, password)

# Define a route for user registration
@app.route('/register', methods=['POST'])
def register():
    try:
        # Get the username and password from the request body
        username = request.json['username']
        password = request.json['password']

        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            return jsonify({'error': 'Username already exists'}), 400

        # Hash the password
        hashed_password = hash_password(password)

        # Create a new user document
        user = {
            'username': username,
            'password': hashed_password
        }

        # Insert the user document into the database
        users_collection.insert_one(user)

        # Return a success message
        return jsonify({'message': 'User created'}), 201
    except Exception as e:
        # Return an error message
        return jsonify({'error': str(e)}), 500

# Define a route for user login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the username and password from the request body
        username = request.json['username']
        password = request.json['password']

        # Find the user document
        user = users_collection.find_one({'username': username})

        # Check if the user exists
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Compare the password with the hashed password
        if not compare_password(password, user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Create an access token
        access_token = create_access_token(identity=str(user['_id']))

        # Return the access token
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        # Return an error message
        return jsonify({'error': str(e)}), 500

# Define a route for protected routes
@app.route('/profile', methods=['GET'])
@jwt_required
def profile():
    try:
        # Get the user ID from the JWT token
        user_id = get_jwt_identity()

        # Find the user document
        user = users_collection.find_one({'_id': ObjectId(user_id)})

        # Check if the user exists
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Return the user document
        return jsonify({'username': user['username']}), 200
    except Exception as e:
        # Return an error message
        return jsonify({'error': str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)