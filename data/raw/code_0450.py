"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_003.txt
Run      : 2
"""

from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Initialize Flask app
app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'YOUR_EMAIL'
app.config['MAIL_PASSWORD'] = 'YOUR_PASSWORD'

# Initialize email client
mail = Mail(app)

# Serializer for generating confirmation tokens
s = URLSafeTimedSerializer('YOUR_SECRET_KEY')

# Database (in-memory for simplicity)
subscriptions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        email = request.form['email']
        # Check if email is already subscribed
        if email in subscriptions:
            return 'Email already subscribed.'
        
        # Generate confirmation token
        token = s.dumps(email)
        
        # Send confirmation email
        send_confirmation_email(email, token)
        
        # Store subscription
        subscriptions[email] = token
        
        return 'Subscription successful. Please check your email for confirmation.'
    
    except Exception as e:
        return str(e)

@app.route('/confirm/<token>')
def confirm(token):
    try:
        # Verify token
        email = s.loads(token)
        
        # Update subscription status
        subscriptions[email] = token
        
        return 'Email confirmed. You can now manage your preferences.'
    
    except Exception as e:
        return str(e)

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    try:
        email = request.form['email']
        # Check if email is subscribed
        if email not in subscriptions:
            return 'Email not found.'
        
        # Send preference email
        send_preference_email(email)
        
        return 'Preference email sent.'
    
    except Exception as e:
        return str(e)

def send_confirmation_email(email, token):
    # Use a real SMTP server or Gmail's SMTP server
    msg = MIMEMultipart()
    msg['From'] = 'YOUR_EMAIL'
    msg['To'] = email
    msg['Subject'] = 'Confirm Your Newsletter Subscription'
    
    body = f'Click this link to confirm your subscription: http://localhost:5000/confirm/{token}'
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('YOUR_EMAIL', 'YOUR_PASSWORD')
    text = msg.as_string()
    server.sendmail('YOUR_EMAIL', email, text)
    server.quit()

def send_preference_email(email):
    # Use a real SMTP server or Gmail's SMTP server
    msg = MIMEMultipart()
    msg['From'] = 'YOUR_EMAIL'
    msg['To'] = email
    msg['Subject'] = 'Manage Your Email Preferences'
    
    body = 'You can now manage your email preferences.'
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('YOUR_EMAIL', 'YOUR_PASSWORD')
    text = msg.as_string()
    server.sendmail('YOUR_EMAIL', email, text)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)