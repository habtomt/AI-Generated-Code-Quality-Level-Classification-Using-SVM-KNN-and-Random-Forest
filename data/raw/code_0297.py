"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_000.txt
Run      : 2
"""

import os
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}')"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Check if passwords match
    if password != confirm_password:
        return 'Passwords do not match', 400

    # Check if email is already registered
    if User.query.filter_by(email=email).first():
        return 'Email already registered', 400

    # Generate verification token
    token = str(uuid.uuid4())

    # Create new user
    user = User(email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    # Send verification email
    send_email(email, token)

    return 'Verification email sent successfully', 200

@app.route('/verify/<token>', methods=['GET'])
def verify(token):
    user = User.query.filter_by(email=request.remote_addr).first()
    if user and user.verified:
        return 'Email already verified', 200
    if user and user.token == token:
        user.verified = True
        db.session.commit()
        return 'Email verified successfully', 200
    return 'Invalid token', 400

def send_email(email, token):
    from_email = 'your_email@gmail.com'
    password = 'your_password'
    to_email = email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Verify Your Email'

    body = f'Click on this link to verify your email: http://localhost:5000/verify/{token}'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)