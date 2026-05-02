"""
Auto-generated Python code
Scenario : Voice & Video Communication
Prompt   : response_003.txt
Run      : 3
"""

# Import necessary libraries
import os
import uuid
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
from pytz import timezone
import pytz
from datetime import date
from datetime import datetime
from pytz import timezone
import smtplib
from email.message import EmailMessage
import base64

# Create a new Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemedicine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins='*')
auth = HTTPBasicAuth()
login_manager = LoginManager(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_doctor = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)

# Medical record model
class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    record = db.Column(db.Text, nullable=False)

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

# Token generation
def generate_token(user):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'iat': datetime.utcnow(),
        'sub': user.id
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# Video call route
@app.route('/video_call', methods=['POST'])
@login_required
def video_call():
    # Get video call data
    data = request.get_json()
    doctor_id = data['doctor_id']
    patient_id = data['patient_id']

    # Connect to video call
    emit('connect', {'doctor_id': doctor_id, 'patient_id': patient_id}, room=str(patient_id))

    # Return success message
    return jsonify({'message': 'Video call connected'})

# Appointment scheduling route
@app.route('/schedule_appointment', methods=['POST'])
@login_required
def schedule_appointment():
    # Get appointment data
    data = request.get_json()
    doctor_id = data['doctor_id']
    patient_id = data['patient_id']
    date = data['date']
    time = data['time']

    # Create new appointment
    appointment = Appointment(doctor_id=doctor_id, patient_id=patient_id, date=date, time=time)
    db.session.add(appointment)
    db.session.commit()

    # Return success message
    return jsonify({'message': 'Appointment scheduled'})

# Medical record sharing route
@app.route('/share_record', methods=['POST'])
@login_required
def share_record():
    # Get medical record data
    data = request.get_json()
    patient_id = data['patient_id']
    doctor_id = data['doctor_id']
    record = data['record']

    # Create new medical record
    medical_record = MedicalRecord(patient_id=patient_id, doctor_id=doctor_id, record=record)
    db.session.add(medical_record)
    db.session.commit()

    # Return success message
    return jsonify({'message': 'Medical record shared'})

# SocketIO event handlers
@socketio.on('connect')
def on_connect(data):
    # Get video call data
    doctor_id = data['doctor_id']
    patient_id = data['patient_id']

    # Connect to video call
    emit('connect', {'doctor_id': doctor_id, 'patient_id': patient_id}, room=str(patient_id))

@socketio.on('disconnect')
def on_disconnect():
    # Get user ID
    user_id = request.sid

    # Disconnect from video call
    emit('disconnect', {'user_id': user_id}, room=str(user_id))

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, host='localhost', port=5000)