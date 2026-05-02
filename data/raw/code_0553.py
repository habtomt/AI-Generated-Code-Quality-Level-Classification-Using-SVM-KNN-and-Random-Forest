"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_002.txt
Run      : 3
"""

# Required imports for payment integration
import requests
import json

# API endpoint for payment gateway
PAYMENT_GATEWAY_API = "https://api.paymentgateway.com/v1/transactions"

# Set API key for authentication
API_KEY = "YOUR_API_KEY"

# Function to handle payment using mobile wallet
def handle_payment(amount, mobile_wallet):
    try:
        # Set API headers with API key
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Set transaction details in JSON format
        transaction_data = {
            "amount": amount,
            "mobile_wallet": mobile_wallet,
            "description": "Transaction for mobile wallet"
        }

        # Send POST request to payment gateway API
        response = requests.post(PAYMENT_GATEWAY_API, headers=headers, data=json.dumps(transaction_data))

        # Check if transaction was successful
        if response.status_code == 200:
            print("Transaction successful!")
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle any exception during API request
        print(f"Error: {e}")
        return None


# Function to handle payment using credit/debit card
def handle_card_payment(amount, card_number, expiry_date, cvv):
    try:
        # Set API headers with API key
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Set transaction details in JSON format
        transaction_data = {
            "amount": amount,
            "card_number": card_number,
            "expiry_date": expiry_date,
            "cvv": cvv,
            "description": "Transaction for credit/debit card"
        }

        # Send POST request to payment gateway API
        response = requests.post(PAYMENT_GATEWAY_API, headers=headers, data=json.dumps(transaction_data))

        # Check if transaction was successful
        if response.status_code == 200:
            print("Transaction successful!")
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle any exception during API request
        print(f"Error: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Example payment using mobile wallet (e.g. Paytm)
    mobile_wallet_payment = handle_payment(100, "paytm")
    if mobile_wallet_payment:
        print(json.dumps(mobile_wallet_payment, indent=4))

    # Example payment using credit/debit card
    card_payment = handle_card_payment(100, "1234567890123456", "12/2025", "123")
    if card_payment:
        print(json.dumps(card_payment, indent=4))