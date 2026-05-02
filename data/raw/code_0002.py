import sqlite3
import hashlib
import os
import random
import time

DB_NAME = "users_mfa.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
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

def generate_mfa_code():
    return str(random.randint(100000, 999999))

def send_mfa_code(email, code):
    print(f"[SIMULATION] MFA code sent to {email}: {code}")

def signup(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, password_hash))
        conn.commit()
        print("Signup successful.")
    except sqlite3.IntegrityError:
        print("Email already exists.")
    finally:
        conn.close()

def login(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if user:
        stored_password = user[0]
        if verify_password(stored_password, password):
            code = generate_mfa_code()
            send_mfa_code(email, code)

            start_time = time.time()
            user_code = input("Enter MFA code: ")

            if time.time() - start_time > 120:
                print("Code expired.")
            elif user_code == code:
                print("Login successful with MFA.")
            else:
                print("Invalid MFA code.")
        else:
            print("Invalid password.")
    else:
        print("User not found.")

    conn.close()

if __name__ == "__main__":
    init_db()

    while True:
        print("\n1. Signup\n2. Login\n3. Exit")
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
            break
