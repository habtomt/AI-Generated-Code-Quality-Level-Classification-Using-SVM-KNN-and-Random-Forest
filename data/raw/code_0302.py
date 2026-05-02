"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import sqlite3
import secrets
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib
import re

# Create a connection to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, email text, password text)''')
conn.commit()

def generate_password(length=12):
    """Generate a secure password of given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def send_email(subject, message, from_addr, to_addr, password):
    """Send an email using the smtplib library."""
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

def email_verification(email, verification_code):
    """Send an email with a verification code."""
    subject = 'Email Verification'
    message = f'Hello, your verification code is: {verification_code}'
    from_addr = 'YOUR_EMAIL@gmail.com'  # Replace with your email
    password = 'YOUR_PASSWORD'  # Replace with your password
    send_email(subject, message, from_addr, email, password)

def signup():
    """Handle user signup process."""
    email = input('Enter your email: ')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print('Invalid email address.')
        return
    password = input('Enter your password: ')
    confirmation = input('Confirm your password: ')
    if password != confirmation:
        print('Passwords do not match.')
        return
    verification_code = generate_password(6)  # Generate a 6-digit code
    email_verification(email, verification_code)
    print('Email sent. Please verify your email address.')
    while True:
        verification_input = input('Enter your verification code: ')
        if verification_input == verification_code:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            print('Account created successfully.')
            break
        else:
            print('Invalid verification code. Please try again.')

def login():
    """Handle user login process."""
    email = input('Enter your email: ')
    password = input('Enter your password: ')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    if user and user[2] == hashed_password:
        print('Login successful.')
    else:
        print('Invalid email or password.')

def main():
    while True:
        print('1. Signup')
        print('2. Login')
        print('3. Quit')
        choice = input('Choose an option: ')
        if choice == '1':
            signup()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('An error occurred:', e)
    finally:
        conn.close()