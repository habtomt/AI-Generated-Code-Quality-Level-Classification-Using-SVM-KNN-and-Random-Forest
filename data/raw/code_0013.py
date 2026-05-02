#!/usr/bin/env python3

import hashlib
import logging
from functools import wraps
from cryptography.fernet import Fernet
import json
import time


# ---------------------------
# AUDIT LOGGING SETUP
# ---------------------------

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def audit_log(action, user, status):
    logging.info(f"USER={user} ACTION={action} STATUS={status}")


# ---------------------------
# ENCRYPTION (AT REST)
# ---------------------------

class EncryptionManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self.cipher.decrypt(token.encode()).decode()


# ---------------------------
# AUTHENTICATION
# ---------------------------

class AuthManager:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password, role):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = {"password": hashed, "role": role}

    def authenticate(self, username, password):
        if username not in self.users:
            return False
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return self.users[username]["password"] == hashed

    def get_role(self, username):
        return self.users.get(username, {}).get("role")


# ---------------------------
# RBAC DECORATOR
# ---------------------------

def require_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(self, username, *args, **kwargs):
            role = self.auth.get_role(username)
            if role != required_role and role != "admin":
                audit_log(func.__name__, username, "DENIED")
                raise PermissionError("Access denied")
            audit_log(func.__name__, username, "GRANTED")
            return func(self, username, *args, **kwargs)
        return wrapper
    return decorator


# ---------------------------
# CLOUD DB CONFIG SIMULATION
# ---------------------------

class CloudDatabase:
    def __init__(self, auth_manager, encryption_manager):
        self.auth = auth_manager
        self.enc = encryption_manager
        self.storage = {}
        self.tls_enabled = True  # encryption in transit simulation

    @require_role("writer")
    def write_data(self, username, key, value):
        if not self.tls_enabled:
            raise Exception("Insecure connection")

        encrypted_value = self.enc.encrypt(value)
        self.storage[key] = encrypted_value

        audit_log("WRITE", username, "SUCCESS")
        return True

    @require_role("reader")
    def read_data(self, username, key):
        if not self.tls_enabled:
            raise Exception("Insecure connection")

        if key not in self.storage:
            audit_log("READ", username, "NOT_FOUND")
            return None

        decrypted = self.enc.decrypt(self.storage[key])
        audit_log("READ", username, "SUCCESS")
        return decrypted


# ---------------------------
# DEMO USAGE
# ---------------------------

def main():
    auth = AuthManager()
    enc = EncryptionManager()

    db = CloudDatabase(auth, enc)

    auth.register_user("alice", "password123", "admin")
    auth.register_user("bob", "pass456", "writer")
    auth.register_user("carol", "pass789", "reader")

    db.write_data("bob", "user1", "sensitive_data_123")
    print(db.read_data("carol", "user1"))

    try:
        db.write_data("carol", "user2", "should_fail")
    except Exception as e:
        print("Access error:", e)

    print("Simulation complete")


if __name__ == "__main__":
    main()