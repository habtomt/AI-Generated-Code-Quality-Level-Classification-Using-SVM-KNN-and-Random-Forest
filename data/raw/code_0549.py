"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_003.txt
Run      : 2
"""

# Import required libraries
import requests
import json
from datetime import datetime

# Placeholder API keys for Stripe and PayPal
STRIPE_API_KEY = "YOUR_STRIPE_API_KEY"
PAYPAL_API_KEY = "YOUR_PAYPAL_API_KEY"

class PaymentProcessor:
    def __init__(self):
        self.stripe_api_key = STRIPE_API_KEY
        self.paypal_api_key = PAYPAL_API_KEY

    # Function to process payment using Stripe
    def process_payment_stripe(self, amount, currency, card_number, exp_month, exp_year, cvc):
        try:
            # Set API endpoint URL
            url = "https://api.stripe.com/v1/charges"

            # Set API headers
            headers = {
                "Authorization": f"Bearer {self.stripe_api_key}",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            # Set API payload
            payload = {
                "amount": amount,
                "currency": currency,
                "card[number]": card_number,
                "card[exp_month]": exp_month,
                "card[exp_year]": exp_year,
                "card[cvc]": cvc
            }

            # Send API request
            response = requests.post(url, headers=headers, data=payload)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = json.loads(response.text)
                return data["id"]
            else:
                # Handle error
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            # Handle request exception
            return f"Error: {e}"

    # Function to process payment using PayPal
    def process_payment_paypal(self, amount, currency, payer_id, token):
        try:
            # Set API endpoint URL
            url = "https://api.paypal.com/v1/payments/payment"

            # Set API headers
            headers = {
                "Authorization": f"Bearer {self.paypal_api_key}",
                "Content-Type": "application/json"
            }

            # Set API payload
            payload = {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [
                    {
                        "amount": {
                            "total": amount,
                            "currency": currency,
                            "details": {
                                "subtotal": amount,
                                "tax": 0,
                                "shipping": 0
                            }
                        },
                        "item_list": {
                            "items": [
                                {
                                    "name": "Test Item",
                                    "price": amount,
                                    "currency": currency,
                                    "quantity": 1
                                }
                            ]
                        }
                    }
                ],
                "redirect_urls": {
                    "return_url": "http://localhost:8080",
                    "cancel_url": "http://localhost:8080"
                }
            }

            # Send API request
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # Check if the request was successful
            if response.status_code == 201:
                # Parse JSON response
                data = json.loads(response.text)
                return data["id"]
            else:
                # Handle error
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            # Handle request exception
            return f"Error: {e}"

# Usage example
payment_processor = PaymentProcessor()
stripe_amount = 1000
stripe_currency = "USD"
paypal_amount = 500
paypal_currency = "EUR"

# Process payment using Stripe
stripe_token = payment_processor.process_payment_stripe(
    amount=stripe_amount,
    currency=stripe_currency,
    card_number="4242424242424242",
    exp_month="12",
    exp_year="2025",
    cvc="123"
)

# Process payment using PayPal
paypal_payer_id = "PAYPAL_PAYER_ID"
paypal_token = "PAYPAL_TOKEN"
paypal_payment_id = payment_processor.process_payment_paypal(
    amount=paypal_amount,
    currency=paypal_currency,
    payer_id=paypal_payer_id,
    token=paypal_token
)

print(f"Stripe payment ID: {stripe_token}")
print(f"PayPal payment ID: {paypal_payment_id}")