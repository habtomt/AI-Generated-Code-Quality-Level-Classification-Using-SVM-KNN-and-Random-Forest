"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_002.txt
Run      : 2
"""

# Import required libraries
import os
import json
import requests
from flask import Flask, render_template, redirect, url_for
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask-bootstrap import Bootstrap
from authlib.integrations.flask_oauth2 import current_token, OAuth2Provider
from authlib.integrations.flask_oauth2 import AuthorizationServer, BearerTokenValidator
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from wtforms.fields.core import IntegerField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize session and database
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define user model
class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    profile_picture = Column(String(200))

    def __repr__(self):
        return f'User({self.username})'

# Define social media provider models
class FacebookUser(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    access_token = Column(String(200))

class GoogleUser(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    access_token = Column(String(200))

# Define login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Define registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# Define OAuth providers
providers = {
    'facebook': 'https://graph.facebook.com/v13.0/me',
    'google': 'https://www.googleapis.com/oauth2/v2/userinfo'
}

# Define OAuth client IDs and secrets
client_ids = {
    'facebook': 'YOUR_FACEBOOK_CLIENT_ID',
    'google': 'YOUR_GOOGLE_CLIENT_ID'
}
client_secrets = {
    'facebook': 'YOUR_FACEBOOK_CLIENT_SECRET',
    'google': 'YOUR_GOOGLE_CLIENT_SECRET'
}

# Define authorization and token endpoints
auth = AuthorizationServer(app, BearerTokenValidator(db))
token_endpoints = {
    'facebook': 'http://localhost:5000/facebook/token',
    'google': 'http://localhost:5000/google/token'
}

# Initialize OAuth providers
facebook_provider = OAuth2Provider(app, client_id=client_ids['facebook'],
                                   client_secret=client_secrets['facebook'],
                                   authorization_base_url='http://localhost:5000/facebook/login',
                                   token_url=token_endpoints['facebook'],
                                   provider_name='facebook')
google_provider = OAuth2Provider(app, client_id=client_ids['google'],
                                  client_secret=client_secrets['google'],
                                  authorization_base_url='http://localhost:5000/google/login',
                                  token_url=token_endpoints['google'],
                                  provider_name='google')

# Define login and logout routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Define registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Define index route
@app.route('/')
@login_required
def index():
    return 'Welcome, ' + current_user.username

# Define OAuth login routes
@app.route('/facebook/login')
def facebook_login():
    return facebook_provider.authorize_redirect(redirect_uri='http://localhost:5000/facebook/callback')

@app.route('/facebook/callback')
def facebook_callback():
    token = facebook_provider.authorize_access_token_response().access_token
    facebook_user = FacebookUser.query.filter_by(user_id=current_user.id).first()
    if not facebook_user:
        facebook_user = FacebookUser(user_id=current_user.id, access_token=token)
        db.session.add(facebook_user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/google/login')
def google_login():
    return google_provider.authorize_redirect(redirect_uri='http://localhost:5000/google/callback')

@app.route('/google/callback')
def google_callback():
    token = google_provider.authorize_access_token_response().access_token
    google_user = GoogleUser.query.filter_by(user_id=current_user.id).first()
    if not google_user:
        google_user = GoogleUser(user_id=current_user.id, access_token=token)
        db.session.add(google_user)
        db.session.commit()
    return redirect(url_for('index'))

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Run app
if __name__ == '__main__':
    app.run(debug=True)