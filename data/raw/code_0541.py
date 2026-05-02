"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_000.txt
Run      : 1
"""

# Import necessary libraries
import os
import stripe
from dotenv import load_dotenv
import logging

# Set up logging to handle exceptions and errors
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Setup Stripe key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def process_payment(amount, currency, payment_method_id):
    """
    Process payment using Stripe API.

    Args:
        amount (int): Amount in cents
        currency (str): Currency code (e.g., usd)
        payment_method_id (str): Payment method ID obtained from client-side

    Returns:
        dict: Payment result containing success flag, payment intent, and any error message
    """
    try:
        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in cents
            currency=currency,
            payment_method=payment_method_id,
            confirmation_method='manual',
            confirm=True,
        )
        logging.info(f"Payment processed successfully, PaymentIntent ID: {intent.id}")
        return {
            'success': True,
            'payment_intent': intent,
        }
    except stripe.error.CardError as e:
        logging.error(f"Payment failed due to: {e.user_message}")
        return {
            'success': False,
            'error': e.user_message
        }
    except Exception as e:
        # Handle different errors accordingly
        logging.error(f"Error processing payment: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Example usage
if __name__ == "__main__":
    # Replace with actual payment method ID obtained from client-side
    payment_method_id = os.getenv('PAYMENT_METHOD_ID')

    # Replace with actual amount and currency
    amount = 5000  # Amount in cents (e.g., $50.00)
    currency = 'usd'

    result = process_payment(amount, currency, payment_method_id)
    
    if result['success']:
        print("Payment processed successfully")
    else:
        print("Payment failed due to:", result['error'])