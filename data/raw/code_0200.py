# newsletter_management.py
import uuid
from email.message import EmailMessage

class NewsletterSystem:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, name, email):
        user_id = str(uuid.uuid4())
        self.subscribers[user_id] = {"name": name, "email": email, "preferences": "all"}
        self.send_confirmation(email, user_id)

    def send_confirmation(self, email, user_id):
        pref_link = f"https://example.com/manage/{user_id}"
        msg = EmailMessage()
        msg.set_content(f"Welcome! Manage your preferences here: {pref_link}")
        msg['Subject'] = "Subscription Confirmed"
        msg['To'] = email
        print(f"Confirmation sent to {email}. Link: {pref_link}")

if __name__ == "__main__":
    news_system = NewsletterSystem()
    news_system.subscribe("Eve", "eve@example.com")