"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_003.txt
Run      : 2
"""

# Import required libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import jwt
import time
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Create a new Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database for users
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define a PasswordReset model
class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(120), nullable=False)
    expires_at = db.Column(db.Float, nullable=False)

# Function to send email with password reset link
def send_password_reset_link(user_email):
    # Generate a new password reset token
    user = User.query.filter_by(email=user_email).first()
    token = jwt.encode({'user_id': user.id, 'expires_at': time.time() + 3600}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    
    # Save the token to the database
    password_reset = PasswordReset(user_id=user.id, token=token, expires_at=time.time() + 3600)
    db.session.add(password_reset)
    db.session.commit()

    # Send email with password reset link
    msg = MIMEMultipart()
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = user_email
    msg['Subject'] = 'Password Reset Link'

    # Create a password reset link
    password_reset_link = f'http://localhost:5000/reset-password?token={token}'

    # Add the password reset link to the email body
    body = f'Please click on the link below to reset your password:\n\n{password_reset_link}'
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    text = msg.as_string()
    server.sendmail('your-email@gmail.com', user_email, text)
    server.quit()

# Route for password reset request
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    # Check if the token is valid
    if request.method == 'POST':
        token = request.form['token']
        try:
            # Decode the token
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
            user = User.query.get(user_id)

            # Check if the token has expired
            password_reset = PasswordReset.query.filter_by(user_id=user_id, token=token).first()
            if password_reset and password_reset.expires_at > time.time():
                # Reset the password
                new_password = request.form['new_password']
                user.password = generate_password_hash(new_password)
                db.session.commit()

                # Delete the password reset token
                db.session.delete(password_reset)
                db.session.commit()

                return 'Password reset successfully.'
            else:
                return 'Invalid token.'
        except jwt.ExpiredSignatureError:
            return 'Token has expired.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'
    else:
        token = request.args.get('token')
        return render_template('reset_password.html', token=token)

# Route for password reset request
@app.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    user_email = request.form['email']
    # Check if the user exists
    user = User.query.filter_by(email=user_email).first()
    if user:
        # Send the password reset link
        send_password_reset_link(user_email)
        return 'Password reset link sent to your email.'
    else:
        return 'User not found.'

# Run the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)