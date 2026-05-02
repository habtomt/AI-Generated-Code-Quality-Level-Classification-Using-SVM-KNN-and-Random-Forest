"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_000.txt
Run      : 1
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)
db = SQLAlchemy(app)

# Serializer for generating and verifying email tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)


# Create the database
@app.before_first_request
def create_tables():
    db.create_all()


# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email is already registered.')
                return redirect(url_for('signup'))

            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            token = serializer.dumps(email, salt='email-confirm-salt')
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('verify_email.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            
            send_email(email, subject, html)

            flash('A confirmation email has been sent to your email address.')
            return redirect(url_for('signup'))
        except Exception as e:
            flash('An error occurred: ' + str(e))
            return redirect(url_for('signup'))

    return render_template('signup.html')


# Route for email confirmation
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt="email-confirm-salt", max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('signup'))

    user = User.query.filter_by(email=email).first()

    if user.is_verified:
        flash('Account already confirmed. Please login.')
    else:
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        flash('Your account has been confirmed.')

    return redirect(url_for('signup'))


def send_email(to, subject, template):
    try:
        msg = Message(subject, recipients=[to], html=template, sender=app.config['MAIL_USERNAME'])
        mail.send(msg)
    except Exception as e:
        flash('Error sending email: ' + str(e))


if __name__ == '__main__':
    app.run(debug=True)