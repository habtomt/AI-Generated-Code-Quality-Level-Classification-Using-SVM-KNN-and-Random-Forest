"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_002.txt
Run      : 3
"""

import os
import shutil
import hashlib
import hmac
import base64
import time
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Set up a secure key for encryption
def generate_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    return private_pem, public_pem

private_key, public_key = generate_key()

# Create a file system class
class FileSystem:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.file_metadata = {}

    def add_file(self, file_path):
        # Calculate file hash and metadata
        file_hash = self.calculate_hash(file_path)
        file_metadata = {
            'hash': file_hash,
            'size': os.path.getsize(file_path),
            'last_modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
        }
        self.file_metadata[file_path] = file_metadata
        # Encrypt file and store it in the file system
        encrypted_file = self.encrypt_file(file_path)
        shutil.copy(encrypted_file, os.path.join(self.root_dir, os.path.basename(file_path)))
        os.remove(encrypted_file)

    def calculate_hash(self, file_path):
        # Calculate file hash using SHA-256
        hash_object = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_object.update(chunk)
        return hash_object.hexdigest()

    def encrypt_file(self, file_path):
        # Encrypt file using Fernet
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        with open(file_path, 'rb') as f:
            file_data = f.read()
        encrypted_file_data = cipher_suite.encrypt(file_data)
        with open('temp_file', 'wb') as f:
            f.write(encrypted_file_data)
        return 'temp_file'

    def decrypt_file(self, file_path):
        # Decrypt file using Fernet
        with open(file_path, 'rb') as f:
            encrypted_file_data = f.read()
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        decrypted_file_data = cipher_suite.decrypt(encrypted_file_data)
        with open('temp_file', 'wb') as f:
            f.write(decrypted_file_data)
        return 'temp_file'

    def get_file(self, file_path):
        # Get file metadata and decrypted file data
        file_metadata = self.file_metadata.get(file_path)
        if file_metadata:
            decrypted_file = self.decrypt_file(os.path.join(self.root_dir, os.path.basename(file_path)))
            return file_metadata, decrypted_file

# Create a file system instance
file_system = FileSystem('/path/to/file/system')

# Add files to the file system
file_system.add_file('/path/to/file1.txt')
file_system.add_file('/path/to/file2.txt')

# Get file metadata and decrypted file data
file_metadata, decrypted_file = file_system.get_file('/path/to/file1.txt')
print(json.dumps(file_metadata, indent=4))
with open(decrypted_file, 'rb') as f:
    print(f.read())