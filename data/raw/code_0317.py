"""
Auto-generated Python code
Scenario : Blockchain & Cryptocurrency
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries for cryptographic operations and blockchain interactions
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import hashlib
import base64
import json
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Set up Flask app and database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallet.db'
db = SQLAlchemy(app)

class DigitalWallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.String(100), unique=True)
    private_key = db.Column(db.String(100))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('digital_wallet.id'))
    sender = db.relationship('DigitalWallet', foreign_keys=[sender_id])
    recipient_id = db.Column(db.Integer, db.ForeignKey('digital_wallet.id'))
    recipient = db.relationship('DigitalWallet', foreign_keys=[recipient_id])
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

# Generate public and private keys for digital wallet
def generate_keys():
    # Generate a new EC key pair
    key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.Pem,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    private_key = key.private_bytes(
        encoding=serialization.Encoding.Pem,
        format=serialization.PrivateFormat.Pkcs8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return public_key, private_key

# Encrypt private key using Fernet
def encrypt_private_key(private_key):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_private_key = cipher_suite.encrypt(private_key)
    return key, encrypted_private_key

# Decrypt private key using Fernet
def decrypt_private_key(private_key, encryption_key):
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(private_key)

# Create digital wallet
@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    public_key, private_key = generate_keys()
    encrypted_private_key = encrypt_private_key(private_key)
    wallet = DigitalWallet(public_key=public_key, private_key=encrypted_private_key[0])
    db.session.add(wallet)
    db.session.commit()
    return jsonify({'public_key': public_key.decode('utf-8'), 'private_key': encrypted_private_key[1].decode('utf-8')})

# Process payment
@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Get sender and recipient public keys from request body
        sender_public_key = request.json['sender_public_key']
        recipient_public_key = request.json['recipient_public_key']
        amount = request.json['amount']
        
        # Verify sender and recipient public keys
        sender = DigitalWallet.query.filter_by(public_key=sender_public_key).first()
        recipient = DigitalWallet.query.filter_by(public_key=recipient_public_key).first()
        
        if sender and recipient:
            # Create transaction
            transaction = Transaction(sender=sender, recipient=recipient, amount=amount, timestamp=datetime.now())
            db.session.add(transaction)
            db.session.commit()
            return jsonify({'message': 'Transaction processed successfully'})
        else:
            return jsonify({'message': 'Invalid sender or recipient public key'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)