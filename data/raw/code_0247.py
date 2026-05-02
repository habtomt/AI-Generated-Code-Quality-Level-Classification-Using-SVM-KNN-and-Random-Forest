import csv
import time
from datetime import datetime

class PromotionalSMSSystem:
    def __init__(self):
        # Subscriber list: Each entry is (Name, Phone, SubscriptionStatus)
        self.subscribers = [
            {"name": "Alice Johnson", "phone": "+12025550101", "active": True},
            {"name": "Mark Spencer", "phone": "+12025550102", "active": True},
            {"name": "Sarah Miller", "phone": "+12025550103", "active": False},
            {"name": "David Chen", "phone": "+12025550104", "active": True}
        ]
        self.campaign_log = []

    def send_sms_via_provider(self, phone, message):
        """Simulates integration with an SMS API (e.g., Twilio, Vonage)."""
        print(f"[TRANSMITTING] To: {phone} | Content: {message}")
        return True

    def run_promotional_campaign(self, offer_title, discount_code):
        print(f"--- Launching Campaign: {offer_title} ---")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messages_sent = 0

        for sub in self.subscribers:
            if sub["active"]:
                personal_message = (
                    f"Hi {sub['name']}! Use code {discount_code} for {offer_title}. "
                    f"Shop now: https://bit.ly/example-shop. Reply STOP to opt-out."
                )
                
                success = self.send_sms_via_provider(sub["phone"], personal_message)
                if success:
                    messages_sent += 1
                
                # Slight delay to respect provider rate limits
                time.sleep(0.1)

        self.campaign_log.append({
            "campaign": offer_title,
            "date": timestamp,
            "recipients": messages_sent
        })
        
        print(f"\nCampaign Complete. Total messages sent: {messages_sent}\n")

    def add_subscriber(self, name, phone):
        self.subscribers.append({"name": name, "phone": phone, "active": True})

# --- Main Execution ---
if __name__ == "__main__":
    marketing_system = PromotionalSMSSystem()

    # Add a new lead
    marketing_system.add_subscriber("Emma Wilson", "+12025550199")

    # Run the promotional blast
    marketing_system.run_promotional_campaign(
        offer_title="20% OFF Spring Collection",
        discount_code="SPRING20"
    )

    # Secondary Flash Sale Campaign
    marketing_system.run_promotional_campaign(
        offer_title="Buy 1 Get 1 Free Today Only",
        discount_code="BOGO26"
    )