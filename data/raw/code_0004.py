import sqlite3
import hashlib
import os
import uuid
import time

DB_NAME = "password_reset.db"
TOKEN_EXPIRY_SECONDS = 300  # 5 minutes

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            reset_token TEXT,
            token_expiry INTEGER
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + hashed

def verify_password(stored_password, provided_password):
    salt = stored_password[:16]
    stored_hash = stored_password[16:]
    new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return new_hash == stored_hash

def signup(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password))
        )
        conn.commit()
        print("User registered.")
    except sqlite3.IntegrityError:
        print("Email already exists.")
    finally:
        conn.close()

def request_password_reset(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if user:
        token = str(uuid.uuid4())
        expiry = int(time.time()) + TOKEN_EXPIRY_SECONDS

        cursor.execute(
            "UPDATE users SET reset_token=?, token_expiry=? WHERE email=?",
            (token, expiry, email)
        )
        conn.commit()

        print(f"[SIMULATION] Reset link: http://localhost/reset/{token}")
    else:
        print("User not found.")

    conn.close()

def reset_password(token, new_password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, token_expiry FROM users WHERE reset_token=?",
        (token,)
    )
    user = cursor.fetchone()

    if user:
        email, expiry = user
        if int(time.time()) > expiry:
            print("Token expired.")
        else:
            cursor.execute(
                "UPDATE users SET password_hash=?, reset_token=NULL, token_expiry=NULL WHERE email=?",
                (hash_password(new_password), email)
            )
            conn.commit()
            print("Password reset successful.")
    else:
        print("Invalid token.")

    conn.close()

def login(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if user and verify_password(user[0], password):
        print("Login successful.")
    else:
        print("Invalid credentials.")

    conn.close()

if __name__ == "__main__":
    init_db()

    while True:
        print("\n1. Signup\n2. Login\n3. Request Password Reset\n4. Reset Password\n5. Exit")
        choice = input("Select: ")

        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            signup(email, password)

        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            login(email, password)

        elif choice == "3":
            email = input("Email: ")
            request_password_reset(email)

        elif choice == "4":
            token = input("Reset token: ")
            new_password = input("New password: ")
            reset_password(token, new_password)

        elif choice == "5":
            break
