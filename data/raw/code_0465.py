"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_003.txt
Run      : 2
"""

# Import necessary libraries for encryption and file handling
from cryptography.fernet import Fernet
import base64
import os
import getpass
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import pickle
import shutil

# Function to generate a key pair for encryption
def generate_key_pair():
    # Create a new RSA key pair
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Serialize the private key
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    # Serialize the public key
    public_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    # Return the private and public keys
    return private_pem.decode(), public_pem.decode()

# Function to encrypt a file using the key pair
def encrypt_file(file_path, private_key):
    try:
        # Load the private key
        key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=default_backend()
        )
        # Load the Fernet key from the private key
        fernet_key = base64.urlsafe_b64encode(key.private_bytes(
            encoding=serialization.Encoding.UTF8,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
        # Create a Fernet instance with the key
        fernet = Fernet(fernet_key)
        # Read the file contents
        with open(file_path, 'rb') as file:
            data = file.read()
        # Encrypt the file contents
        encrypted_data = fernet.encrypt(data)
        # Save the encrypted data to a new file
        with open(file_path + '.enc', 'wb') as file:
            file.write(encrypted_data)
        # Return True to indicate successful encryption
        return True
    except Exception as e:
        # Return False to indicate failed encryption
        print(f"Error encrypting file: {e}")
        return False

# Function to decrypt a file using the key pair
def decrypt_file(file_path, private_key):
    try:
        # Load the private key
        key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=default_backend()
        )
        # Load the Fernet key from the private key
        fernet_key = base64.urlsafe_b64encode(key.private_bytes(
            encoding=serialization.Encoding.UTF8,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
        # Create a Fernet instance with the key
        fernet = Fernet(fernet_key)
        # Read the encrypted file contents
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        # Decrypt the file contents
        decrypted_data = fernet.decrypt(encrypted_data)
        # Save the decrypted data to a new file
        with open(file_path[:-4], 'wb') as file:
            file.write(decrypted_data)
        # Return True to indicate successful decryption
        return True
    except Exception as e:
        # Return False to indicate failed decryption
        print(f"Error decrypting file: {e}")
        return False

# Generate a key pair
private_key, public_key = generate_key_pair()

# Encrypt a file
encrypt_file('test.txt', private_key)

# Decrypt the file
decrypt_file('test.txt.enc', private_key)