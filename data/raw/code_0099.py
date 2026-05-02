#!/usr/bin/env python3

import random
import time

# Mock user database
USERS = {
    "ezgi": "password123",
    "testuser": "testpass"
}

# Temporary storage for OTP codes
otp_store = {}

def send_sms(phone_number, code):
    print(f"[SMS to {phone_number}] Your verification code is: {code}")

def generate_otp():
    return str(random.randint(100000, 999999))

def request_login():
    username = input("Username: ")
    password = input("Password: ")

    if username not in USERS or USERS[username] != password:
        print("Invalid username or password.")
        return False

    phone_number = input("Enter your phone number: ")

    otp = generate_otp()
    otp_store[username] = {
        "code": otp,
        "expires": time.time() + 120
    }

    send_sms(phone_number, otp)

    return verify_otp(username)

def verify_otp(username):
    attempts = 3

    while attempts > 0:
        code = input("Enter the verification code sent to your phone: ")

        record = otp_store.get(username)

        if not record:
            print("No OTP found. Please login again.")
            return False

        if time.time() > record["expires"]:
            print("OTP expired.")
            return False

        if code == record["code"]:
            print("Login successful.")
            del otp_store[username]
            return True

        attempts -= 1
        print(f"Incorrect code. Attempts left: {attempts}")

    print("Too many failed attempts.")
    return False


def main():
    print("=== Secure Login System ===")
    success = request_login()

    if not success:
        print("Access denied.")
    else:
        print("Access granted.")

if __name__ == "__main__":
    main()