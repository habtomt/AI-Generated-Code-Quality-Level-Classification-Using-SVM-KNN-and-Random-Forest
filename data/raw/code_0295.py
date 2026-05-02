"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_003.txt
Run      : 1
"""

import os
import jwt
import bcrypt
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_database"
mongo = PyMongo(app)

# Secret key for JWT
secret_key = "YOUR_SECRET_KEY"

# Email configuration
email_host = "YOUR_EMAIL_HOST"
email_port = 587
email_user = "YOUR_EMAIL_USER"
email_pass = "YOUR_EMAIL_PASS"

# Connect to MongoDB
@app.before_first_request
def connect_to_mongo():
    # Ensure the MongoDB connection is established
    mongo.cx = mongo.connect(app.config["MONGO_URI"])

# Define a function to send emails
def send_email(to, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to
    msg["from"] = email_user

    with smtplib.SMTP_SSL(email_host, email_port) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

# Request password reset link
@app.route('/request-reset-password', methods=['POST'])
def request_reset_password():
    data = request.get_json()
    email = data.get('email')
    
    # Find the user by email
    user = mongo.db.users.find_one({"email": email})
    
    if not user:
        return jsonify({"error": "No user found with that email."}), 400

    # Generate a JWT token
    token = jwt.encode({
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }, secret_key, algorithm="HS256")
    
    # Save the token to the user document
    mongo.db.users.update_one({"email": user["email"]}, {"$set": {"resetToken": token, "resetTokenExpiry": datetime.utcnow() + timedelta(hours=1)}})
    
    # Send the reset link via email
    reset_link = f"http://localhost:5000/reset-password?token={token}"
    send_email(user["email"], "Password Reset", f"Please click the link below to reset your password: {reset_link}")
    
    return jsonify({"message": "Password reset link has been sent to your email."})

# Reset password using token
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('newPassword')
    
    try:
        # Verify the token
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Find the user by email and token
        user = mongo.db.users.find_one({
            "email": decoded["email"],
            "resetToken": token,
            "resetTokenExpiry": {"$gt": datetime.utcnow()}
        })
        
        if not user:
            return jsonify({"error": "Invalid or expired token."}), 400
        
        # Hash the new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Update the user's password
        mongo.db.users.update_one({"email": user["email"]}, {"$set": {"password": hashed_password}, "$unset": {"resetToken": "", "resetTokenExpiry": ""}})
        
        return jsonify({"message": "Password has been reset."})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired."}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token."}), 400

if __name__ == '__main__':
    app.run(debug=True)