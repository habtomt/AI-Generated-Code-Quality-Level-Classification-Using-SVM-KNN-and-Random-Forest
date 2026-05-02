"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_001.txt
Run      : 2
"""

import getpass
import pyotp
import requests

class SecureLogin:
    def __init__(self):
        self.api_key = "YOUR_TWO_FACTOR_AUTH_SERVICE_API_KEY"
        self.secret_key = "YOUR_TWO_FACTOR_AUTH_SERVICE_SECRET_KEY"
        self.user_id = "YOUR_USER_ID"

    def get_password(self):
        password = getpass.getpass("Enter password: ")
        return password

    def send_otp(self):
        try:
            response = requests.post(
                f"https://2fa-service.com/send-otp/{self.user_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"secret_key": self.secret_key}
            )
            response.raise_for_status()
            print("OTP sent to your mobile device.")
            return response.json()["otp"]
        except requests.RequestException as e:
            print("Error sending OTP:", e)

    def verify_otp(self):
        otp = input("Enter OTP: ")
        try:
            totp = pyotp.TOTP(self.secret_key)
            if totp.verify(otp):
                print("OTP verified successfully.")
                return True
            else:
                print("Invalid OTP. Please try again.")
                return False
        except pyotp.exceptions.BadTime:
            print("Invalid OTP. Please try again.")
            return False

    def login(self):
        password = self.get_password()
        otp = self.send_otp()
        if not otp:
            return
        if self.verify_otp():
            print("Login successful.")
        else:
            print("Login failed.")

if __name__ == "__main__":
    secure_login = SecureLogin()
    secure_login.login()