"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
import hashlib
import base64
import json
import requests

# Define a Card class to represent a credit card
class Card:
    def __init__(self, number, expiration_date, cvv, name_on_card):
        self.number = number
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.name_on_card = name_on_card

    def hash_card_details(self):
        # SHA-256 hash of card details for verification
        card_details = f"{self.number}{self.expiration_date}{self.cvv}{self.name_on_card}"
        hashed_card_details = hashlib.sha256(card_details.encode()).hexdigest()
        return hashed_card_details

# Define a PaymentGateway class to interact with the payment gateway API
class PaymentGateway:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def verify_card(self, hashed_card_details):
        # Simulate API call to verify card details
        try:
            response = requests.post(
                "https://example.com/verify-card",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                data=json.dumps({"hashed_card_details": hashed_card_details}),
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error verifying card: {e}")
            return None

    def process_payment(self, amount, card):
        # Simulate API call to process payment
        try:
            hashed_card_details = card.hash_card_details()
            verification_response = self.verify_card(hashed_card_details)
            if verification_response["verified"]:
                response = requests.post(
                    "https://example.com/process-payment",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    data=json.dumps({
                        "amount": amount,
                        "card_number": card.number,
                        "expiration_date": card.expiration_date,
                        "cvv": card.cvv,
                        "name_on_card": card.name_on_card,
                    }),
                )
                response.raise_for_status()
                return response.json()
            else:
                print("Card verification failed")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error processing payment: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Replace with your actual API credentials
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"

    # Create a payment gateway instance
    payment_gateway = PaymentGateway(api_key, api_secret)

    # Create a card instance
    card = Card(
        number="4242424242424242",
        expiration_date="12/2025",
        cvv="123",
        name_on_card="John Doe",
    )

    # Process a payment
    amount = 100.00
    payment_response = payment_gateway.process_payment(amount, card)
    if payment_response:
        print("Payment processed successfully")
        print(json.dumps(payment_response, indent=4))
    else:
        print("Payment failed")