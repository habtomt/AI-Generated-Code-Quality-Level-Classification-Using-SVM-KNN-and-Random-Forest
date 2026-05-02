import hashlib
import secrets
import time
from datetime import datetime, timedelta

class PasswordResetSystem:
    def __init__(self):
        # Mock database: {email: {"password": "...", "reset_token": "...", "token_expiry": timestamp}}
        self.users = {
            "dev@example.com": {
                "password": "oldpassword123",
                "reset_token": None,
                "token_expiry": None
            }
        }
        self.token_valid_duration = 300  # 5 minutes in seconds

    def generate_reset_link(self, email):
        if email not in self.users:
            return None
        
        # Generate a secure random token
        token = secrets.token_urlsafe(32)
        expiry = time.time() + self.token_valid_duration
        
        # Store token and expiry in database
        self.users[email]["reset_token"] = token
        self.users[email]["token_expiry"] = expiry
        
        # In a real app, this would be sent via email
        reset_link = f"https://myapp.com/reset-password?email={email}&token={token}"
        return reset_link

    def validate_and_change_password(self, email, token, new_password):
        user = self.users.get(email)
        
        if not user or user["reset_token"] != token:
            return "Error: Invalid email or token."
            
        if time.time() > user["token_expiry"]:
            return "Error: Reset link has expired."
            
        # Update password and clear token
        user["password"] = new_password
        user["reset_token"] = None
        user["token_expiry"] = None
        return "Success: Password has been updated securely."

def run_demo():
    system = PasswordResetSystem()
    target_email = "dev@example.com"
    
    print(f"--- Password Reset System ---")
    print(f"Requesting reset for: {target_email}")
    
    link = system.generate_reset_link(target_email)
    print(f"\nGenerated Secure Link:\n{link}")
    
    # Simulating extracting data from the link (as a web server would)
    # Case 1: Valid Reset
    print(f"\n[Attempt 1] Valid Reset Request...")
    import urllib.parse
    parsed = urllib.parse.urlparse(link)
    params = urllib.parse.parse_qs(parsed.query)
    
    result = system.validate_and_change_password(
        params['email'][0], 
        params['token'][0], 
        "NewSecurePass2024!"
    )
    print(result)
    
    # Case 2: Expired/Invalid Token
    print(f"\n[Attempt 2] Re-using the same token...")
    retry = system.validate_and_change_password(
        params['email'][0], 
        params['token'][0], 
        "AnotherPassword"
    )
    print(retry)

if __name__ == "__main__":
    run_demo()