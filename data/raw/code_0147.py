import sqlite3
import hashlib
import secrets
import smtplib
from email.message import EmailMessage

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0,
            verification_token TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- Security Logic ---
def hash_password(password):
    salt = secrets.token_hex(16)
    pw_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return pw_hash, salt

# --- Email Logic (Mock/Simple) ---
def send_verification_email(receiver_email, token):
    # In a production environment, use actual SMTP credentials
    print(f"\n[SYSTEM] Email sent to {receiver_email}")
    print(f"[SYSTEM] Verification Link: http://myapp.com/verify?token={token}\n")

# --- User Actions ---
def signup(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    pw_hash, salt = hash_password(password)
    token = secrets.token_urlsafe(32)
    
    try:
        cursor.execute('''
            INSERT INTO users (email, password_hash, salt, verification_token)
            VALUES (?, ?, ?, ?)
        ''', (email, pw_hash, salt, token))
        conn.commit()
        send_verification_email(email, token)
        print("Registration successful! Please check your email to verify.")
    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
    finally:
        conn.close()

def verify_email(token):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM users WHERE verification_token = ?', (token,))
    user = cursor.fetchone()
    
    if user:
        cursor.execute('''
            UPDATE users 
            SET is_verified = 1, verification_token = NULL 
            WHERE id = ?
        ''', (user[0],))
        conn.commit()
        print("Account verified successfully!")
    else:
        print("Invalid or expired token.")
    
    conn.close()

# --- Execution Flow ---
if __name__ == "__main__":
    init_db()
    
    # 1. User registers
    test_email = "junior_dev@example.com"
    signup(test_email, "SecurePass123!")
    
    # 2. Simulate user clicking the token from the "email"
    conn = sqlite3.connect('users.db')
    token_to_test = conn.execute("SELECT verification_token FROM users WHERE email=?", (test_email,)).fetchone()[0]
    conn.close()
    
    if token_to_test:
        verify_email(token_to_test)