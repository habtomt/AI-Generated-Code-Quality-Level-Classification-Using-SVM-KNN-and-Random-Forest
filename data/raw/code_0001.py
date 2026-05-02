import sqlite3
import hashlib
import os
import smtplib
import ssl
import uuid
from email.message import EmailMessage

DB_NAME = "users.db"
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            verified INTEGER DEFAULT 0,
            verification_token TEXT
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

def send_verification_email(receiver_email, token):
    subject = "Verify your account"
    body = f"Click the link to verify your account:\nhttp://localhost:5000/verify/{token}"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def signup(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    password_hash = hash_password(password)
    token = str(uuid.uuid4())

    try:
        cursor.execute("""
            INSERT INTO users (email, password_hash, verification_token)
            VALUES (?, ?, ?)
        """, (email, password_hash, token))
        conn.commit()
        send_verification_email(email, token)
        print("Signup successful. Please check your email to verify your account.")
    except sqlite3.IntegrityError:
        print("Email already exists.")
    finally:
        conn.close()

def verify_account(token):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE verification_token=?", (token,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET verified=1, verification_token=NULL WHERE id=?", (user[0],))
        conn.commit()
        print("Account verified successfully.")
    else:
        print("Invalid token.")

    conn.close()

def login(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash, verified FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if user:
        stored_password, verified = user
        if not verified:
            print("Please verify your email first.")
        elif verify_password(stored_password, password):
            print("Login successful.")
        else:
            print("Invalid password.")
    else:
        print("User not found.")

    conn.close()

if __name__ == "__main__":
    init_db()

    while True:
        print("\n1. Signup\n2. Verify\n3. Login\n4. Exit")
        choice = input("Select: ")

        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            signup(email, password)

        elif choice == "2":
            token = input("Verification token: ")
            verify_account(token)

        elif choice == "3":
            email = input("Email: ")
            password = input("Password: ")
            login(email, password)

        elif choice == "4":
            break
