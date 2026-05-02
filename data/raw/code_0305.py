"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_003.txt
Run      : 3
"""

# Import required libraries
import re
import smtplib
import hashlib
import secrets
import string
import time
from email.message import EmailMessage
from datetime import datetime, timedelta

# Import a library for generating a secure token
import jwt

# Set email credentials (replace with your actual Gmail account credentials)
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"

# Create a SMTP email object
smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
smtp_server.starttls()
smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

class PasswordResetSystem:
    def __init__(self):
        # Initialize a dictionary to store user credentials
        self.users = {}

    def register_user(self, email, password):
        # Hash the password for secure storage
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create a new user with a unique ID and hashed password
        user_id = self.generate_unique_id()
        self.users[user_id] = {"email": email, "password": hashed_password}

        # Return the user ID for logging in
        return user_id

    def login(self, user_id, password):
        # Hash the input password and compare it with the stored hash
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if self.users.get(user_id, {}).get("password") == hashed_password:
            return True
        else:
            return False

    def request_password_reset(self, email):
        # Check if the user is registered
        for user_id, user in self.users.items():
            if user["email"] == email:
                # Generate a secure token for password reset
                token = self.generate_secure_token(user_id)
                
                # Send a password reset email
                self.send_password_reset_email(email, token)
                
                return True
        return False

    def send_password_reset_email(self, email, token):
        # Create a new email message
        msg = EmailMessage()
        msg.set_content(f"Password Reset Token: {token} (Valid for 15 minutes)")
        msg["Subject"] = "Password Reset Request"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        
        # Send the email using the SMTP server
        smtp_server.sendmail(EMAIL_ADDRESS, email, msg.as_string())

    def validate_token(self, token):
        try:
            # Decode the token to get the user ID
            user_id = jwt.decode(token, verify=True)["user_id"]
            
            # Check if the token is still valid (15-minute expiration time)
            expiration_time = datetime.fromtimestamp(jwt.decode(token, verify=True)["exp"])
            if datetime.now() < expiration_time:
                return user_id
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def change_password(self, user_id, new_password, token):
        # Validate the token
        validated_user_id = self.validate_token(token)
        if validated_user_id is None:
            return False
        
        # Update the user's password
        self.users[user_id]["password"] = hashlib.sha256(new_password.encode()).hexdigest()
        
        return True

    def generate_secure_token(self, user_id):
        # Generate a secure token with a 15-minute expiration time
        expiration_time = int(time.time()) + 15 * 60
        token = jwt.encode({"user_id": user_id, "exp": expiration_time}, secret_key="your_secret_key", algorithm="HS256")
        
        return token

    def generate_unique_id(self):
        # Generate a unique ID for the user
        return secrets.token_hex(16)


# Create an instance of the PasswordResetSystem
password_reset_system = PasswordResetSystem()

# Example usage:
user_id = password_reset_system.register_user("user@example.com", "password123")
password_reset_system.request_password_reset("user@example.com")

# Validate token and change password
token = password_reset_system.generate_secure_token(user_id)
if password_reset_system.change_password(user_id, "new_password", token):
    print("Password changed successfully")
else:
    print("Invalid token or password change failed")

# Close the SMTP connection
smtp_server.quit()