"""
Auto-generated Python code
Scenario : Voice & Video Communication
Prompt   : response_003.txt
Run      : 1
"""

# Import required libraries
import pytz
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import json
from flask_cors import CORS
import os
from cryptography.fernet import Fernet
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemedicine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
socketio = SocketIO(app)
cors = CORS(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    specialty = db.Column(db.String(64), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    medical_record = db.Column(db.String(128), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Define encryption key
encryption_key = os.urandom(32)

# Define routes
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify(error='Invalid credentials'), 401

@app.route('/appointments', methods=['POST'])
@jwt_required
def create_appointment():
    doctor_id = request.json.get('doctor_id')
    patient_id = request.json.get('patient_id')
    date = request.json.get('date')
    appointment = Appointment(doctor_id=doctor_id, patient_id=patient_id, date=date)
    db.session.add(appointment)
    db.session.commit()
    return jsonify(message='Appointment created successfully'), 201

@app.route('/appointments/<int:id>', methods=['GET'])
@jwt_required
def get_appointment(id):
    appointment = Appointment.query.get(id)
    if appointment:
        return jsonify(appointment.to_dict())
    return jsonify(error='Appointment not found'), 404

@app.route('/medical-record', methods=['POST'])
@jwt_required
def update_medical_record():
    patient_id = request.json.get('patient_id')
    medical_record = request.json.get('medical_record')
    patient = Patient.query.get(patient_id)
    if patient:
        patient.medical_record = medical_record
        db.session.commit()
        return jsonify(message='Medical record updated successfully')
    return jsonify(error='Patient not found'), 404

# Define socket.io event
@socketio.on('connect')
def connect():
    emit('message', 'Connected to the server')

# Run app
if __name__ == '__main__':
    db.create_all()
    socketio.run(app)