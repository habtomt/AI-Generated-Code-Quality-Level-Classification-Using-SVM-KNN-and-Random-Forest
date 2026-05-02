"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_003.txt
Run      : 1
"""

import requests
import json
import decimal

class PaymentProcessor:
    def __init__(self, payment_gateway_api_key, compliance_service_api_key):
        self.payment_gateway_api_key = payment_gateway_api_key
        self.compliance_service_api_key = compliance_service_api_key
        self.exchange_rate_api = "https://api.exchangerate-api.com/v4/latest"
        self.decimal_context = decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN)
    
    def convert_currency(self, amount, from_currency, to_currency):
        # Fetch the conversion rate from a reliable source
        response = requests.get(f"{self.exchange_rate_api}?base={from_currency}")
        rates = response.json()['rates']
        rate = rates.get(to_currency)
        if rate is None:
            raise ValueError(f"Unsupported currency: {to_currency}")
        return decimal.Decimal(amount, self.decimal_context) * decimal.Decimal(rate, self.decimal_context)

    def check_compliance(self, user_details):
        # Simulated compliance check - Replace with a real compliance service
        print("Checking compliance for user:", json.dumps(user_details))
        response = requests.post("https://example-compliance-api.com/check", json=user_details,
                                 headers={"Authorization": f"Bearer {self.compliance_service_api_key}"})
        try:
            return response.json()['compliance_status'] == "clear"
        except KeyError:
            raise ValueError("Invalid compliance response")

    def process_payment(self, amount, from_currency, to_currency, user_details, payment_details):
        if not self.check_compliance(user_details):
            raise Exception("Compliance check failed.")

        amount = decimal.Decimal(amount, self.decimal_context)
        converted_amount = self.convert_currency(amount, from_currency, to_currency)
        payment = {
            "amount": float(converted_amount),  # Convert to float for API compatibility
            "currency": to_currency,
            "payee": payment_details['payee'],
            "payer": payment_details['payer']
        }

        # This should be replaced with actual API calls to a payment gateway
        response = requests.post("https://example-payment-gateway.com/process",
                                 json=payment,
                                 headers={"Authorization": f"Bearer {self.payment_gateway_api_key}"})

        try:
            return response.json()
        except json.JSONDecodeError:
            raise ValueError("Invalid response from payment gateway")

# Example Usage
processor = PaymentProcessor("YOUR_PAYMENT_GATEWAY_KEY", "YOUR_COMPLIANCE_SERVICE_KEY")

user_details = {
    "name": "John Doe",
    "country": "US",
    "id_document": "passport_number"
}

payment_details = {
    "payee": "recipient_account_number",
    "payer": "sender_account_number"
}

try:
    result = processor.process_payment(1000, "USD", "EUR", user_details, payment_details)
    print("Payment processed successfully:", json.dumps(result))
except Exception as e:
    print("Error processing payment:", str(e))