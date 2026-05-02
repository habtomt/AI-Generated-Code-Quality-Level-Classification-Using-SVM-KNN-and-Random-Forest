import random
import time

class SMSVerificationSystem:
    def __init__(self):
        # Simulated database of users and their phone numbers
        self.user_db = {
            "alice": "+1234567890",
            "bob": "+1987654321"
        }
        self.pending_verifications = {}

    def send_sms(self, phone_number, code):
        """Simulates sending an SMS via a gateway (e.g., Twilio)."""
        print(f"\n[SMS Gateway] Sending code {code} to {phone_number}...")
        return True

    def initiate_login(self, username):
        if username not in self.user_db:
            print("Error: User not found.")
            return False

        # Generate a 6-digit code
        code = str(random.randint(100000, 999999))
        phone = self.user_db[username]
        
        # Store code with a timestamp for expiration (e.g., 5 minutes)
        self.pending_verifications[username] = {
            "code": code,
            "expires": time.time() + 300
        }

        self.send_sms(phone, code)
        return True

    def verify_code(self, username, user_input):
        record = self.pending_verifications.get(username)

        if not record:
            print("Error: No pending verification found.")
            return False

        if time.time() > record["expires"]:
            print("Error: Verification code expired.")
            del self.pending_verifications[username]
            return False

        if user_input == record["code"]:
            print("Success: Access granted!")
            del self.pending_verifications[username]
            return True
        else:
            print("Error: Incorrect code.")
            return False

# --- Execution Logic ---
if __name__ == "__main__":
    system = SMSVerificationSystem()
    
    user = "alice"
    print(f"--- Login attempt for: {user} ---")
    
    if system.initiate_login(user):
        # In a real app, this input comes from the user interface
        entered_code = input("Enter the 6-digit code received: ")
        system.verify_code(user, entered_code)