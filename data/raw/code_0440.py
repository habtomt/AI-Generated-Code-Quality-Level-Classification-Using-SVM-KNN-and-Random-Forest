"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_003.txt
Run      : 3
"""

from flask import Flask, request, jsonify, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import uuid

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# In-memory user database
users = {}

# Registration endpoint
@app.route("/register", methods=["POST"])
def register():
    try:
        # Get user data
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]

        # Check if username or email already exists
        if username in users or email in [user["email"] for user in users.values()]:
            return jsonify({"error": "Username or email already taken"}), 400

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create new user
        user_id = str(uuid.uuid4())
        users[user_id] = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "session_id": None,
        }

        return jsonify({"message": "User created successfully"}), 201
    except KeyError as e:
        return jsonify({"error": "Missing parameter: " + e.args[0]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Login endpoint
@app.route("/login", methods=["POST"])
def login():
    try:
        # Get user data
        username = request.json["username"]
        password = request.json["password"]

        # Check if user exists
        user = next((user for user in users.values() if user["username"] == username), None)
        if user is None:
            return jsonify({"error": "Invalid username or password"}), 401

        # Check password
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid username or password"}), 401

        # Create session
        session_id = str(uuid.uuid4())
        user["session_id"] = session_id
        session["session_id"] = session_id
        session["user_id"] = user_id

        return jsonify({"message": "Logged in successfully"}), 200
    except KeyError as e:
        return jsonify({"error": "Missing parameter: " + e.args[0]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Profile management endpoint
@app.route("/profile", methods=["GET"])
def profile():
    try:
        # Get user data
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify({"error": "Not logged in"}), 401

        # Get user from database
        user = next((user for user in users.values() if user["session_id"] == session["session_id"]), None)
        if user is None:
            return jsonify({"error": "Invalid session"}), 401

        # Return user data
        return jsonify({"username": user["username"], "email": user["email"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Logout endpoint
@app.route("/logout", methods=["POST"])
def logout():
    try:
        # Get user data
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify({"error": "Not logged in"}), 401

        # Get user from database
        user = next((user for user in users.values() if user["session_id"] == session["session_id"]), None)
        if user is None:
            return jsonify({"error": "Invalid session"}), 401

        # Remove session
        user["session_id"] = None
        session.pop("session_id")
        session.pop("user_id")

        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)