"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_003.txt
Run      : 1
"""

from twilio.rest import Client
import random
import string

# Your Twilio account SID and auth token
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'

# Create a Twilio client
client = Client(account_sid, auth_token)

def send_sms(to_number, message_body):
    # Replace with your Twilio phone number
    from_number = '+12345678901'  # Replace with your Twilio phone number

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"Message sent to {to_number}, Message SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {to_number}: {str(e)}")

def generate_password(length):
    """Generate a random alphanumeric password of a given length."""
    letters_and_digits = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(letters_and_digits) for _ in range(length))
    return password

def notify_customer(inquiry_id, customer_phone, status):
    # Generate the message content based on the inquiry update
    message_body = (
        f"Update for your support inquiry #{inquiry_id}:
"
        f"Current status: {status}. Thank you for your patience."
    )

    # Send SMS notification
    send_sms(customer_phone, message_body)

    # Create a new account and password for the customer to log in
    password_length = 12
    password = generate_password(password_length)
    print(f"Generated password for customer: {password}")

def main():
    # Example usage
    customer_phone_number = '+1234567890'  # Customer's phone number
    inquiry_id = 1001  # Example inquiry ID
    status_update = "Resolved"  # Example status update

    notify_customer(inquiry_id, customer_phone_number, status_update)

if __name__ == "__main__":
    main()