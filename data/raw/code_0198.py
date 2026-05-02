# welcome_sequence.py
from email.message import EmailMessage

def run_welcome_sequence(subscriber):
    sequence = [
        {"subject": "Welcome!", "content": "Thanks for joining. Here is a guide to our products."},
        {"subject": "Pro Tip", "content": "Did you know you can use our API for automation?"},
        {"subject": "Case Study", "content": "See how others are succeeding with us."}
    ]

    for email_data in sequence:
        msg = EmailMessage()
        msg.set_content(f"Hi {subscriber['name']},\n{email_data['content']}")
        msg['Subject'] = email_data['subject']
        msg['To'] = subscriber['email']
        print(f"Sending: {email_data['subject']} to {subscriber['email']}")

subscriber = {'name': 'Charlie', 'email': 'charlie@example.com'}

if __name__ == "__main__":
    run_welcome_sequence(subscriber)