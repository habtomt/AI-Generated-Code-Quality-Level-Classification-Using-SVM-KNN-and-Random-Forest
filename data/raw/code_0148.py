import random
import time
import sys

def mock_send_mfa_code(phone_number):
    """Simulates sending a 6-digit code to a mobile device."""
    code = str(random.randint(100000, 999999))
    print(f"\n[SMS Gateway] Sending MFA code {code} to {phone_number}...")
    return code

def login():
    # Mock user database
    user_db = {
        "junior_dev": {
            "password": "password123",
            "phone": "+1-555-0199"
        }
    }

    print("--- Secure Login System ---")
    username = input("Username: ")
    password = input("Password: ")

    # Step 1: Password Verification
    if username in user_db and user_db[username]["password"] == password:
        print("\n[Step 1] Password verified successfully.")
        
        # Step 2: Multi-Factor Authentication (MFA)
        target_phone = user_db[username]["phone"]
        secret_code = mock_send_mfa_code(target_phone)
        
        print(f"A verification code has been sent to {target_phone[-4:].rjust(len(target_phone), '*')}")
        
        attempts = 3
        while attempts > 0:
            user_input_code = input(f"Enter the 6-digit MFA code (Attempts left: {attempts}): ")
            
            if user_input_code == secret_code:
                print("\n[Step 2] MFA verification successful!")
                print(f"Access Granted. Welcome, {username}!")
                return True
            else:
                attempts -= 1
                print("Invalid code.")
        
        print("\nToo many failed MFA attempts. Access Denied.")
        return False
    else:
        print("\nInvalid username or password.")
        return False

if __name__ == "__main__":
    try:
        login()
    except KeyboardInterrupt:
        print("\nProcess terminated.")
        sys.exit(0)