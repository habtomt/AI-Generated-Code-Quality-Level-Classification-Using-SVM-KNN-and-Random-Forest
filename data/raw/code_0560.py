"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_004.txt
Run      : 1
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import argparse

# Function to get email credentials from command line arguments
def get_credentials():
    parser = argparse.ArgumentParser(description='Email Notification System')
    parser.add_argument('--smtp_server', help='SMTP server', required=True)
    parser.add_argument('--smtp_port', help='SMTP port', type=int, required=True)
    parser.add_argument('--smtp_user', help='SMTP username', required=True)
    parser.add_argument('--smtp_pass', help='SMTP password', required=True)
    args = parser.parse_args()
    return args.smtp_server, args.smtp_port, args.smtp_user, args.smtp_pass

def send_promotional_email(to_email, subject, body, smtp_server, smtp_port, smtp_user, smtp_pass):
    try:
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach email body
        msg.attach(MIMEText(body, 'plain'))

        # Connect to server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def notify_users():
    # Sample user email list
    user_emails = ['user1@example.com', 'user2@example.com']

    # Promotional offer details
    offer = "Get 20% OFF on your next purchase!"
    validity_period = timedelta(days=3)
    expiry_date = (datetime.now() + validity_period).strftime("%Y-%m-%d")

    # Email details
    subject = "Limited Time Offer!"
    body = f"Hello,

We are excited to offer you a special discount: {offer}
Hurry, this offer expires on {expiry_date}.

Best Regards,
Your Company"

    # Get email credentials from command line arguments
    smtp_server, smtp_port, smtp_user, smtp_pass = get_credentials()

    for email in user_emails:
        send_promotional_email(email, subject, body, smtp_server, smtp_port, smtp_user, smtp_pass)

if __name__ == "__main__":
    notify_users()