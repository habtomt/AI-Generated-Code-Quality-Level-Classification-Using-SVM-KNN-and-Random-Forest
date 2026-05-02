"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_000.txt
Run      : 3
"""

# Import required libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz
import json

# Load subscriber data from JSON file
with open('subscribers.json') as f:
    subscribers = json.load(f)

# Define your email credentials (replace with your own credentials)
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_email_password'

# Define your SMTP server configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Define the email template
email_template = '''
Dear {name},

We're excited to offer you an exclusive 15% discount on your next purchase!

As a valued customer, we appreciate your loyalty and commitment to our brand. To redeem your discount, simply use the code {coupon_code} at checkout.

Best regards,
[Your Name]
'''

# Set up the SMTP server
def send_email(subscriber):
    try:
        # Create a message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = subscriber['email']
        msg['Subject'] = 'Exclusive Discount for You!'

        # Format the email body using the email template
        body = email_template.format(
            name=subscriber['name'],
            coupon_code='YOUR_COUPON_CODE'  # Replace with your own coupon code
        )
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, subscriber['email'], text)
        server.quit()

        print(f'Email sent to {subscriber["email"]} successfully!')

    except Exception as e:
        print(f'Error sending email to {subscriber["email"]}: {str(e)}')

# Send promotional emails to subscribers based on their time zone
def send_promotional_emails():
    for subscriber in subscribers:
        try:
            # Get the subscriber's time zone
            tz = pytz.timezone(subscriber['time_zone'])

            # Check if it's 8am in the subscriber's time zone (adjust to your desired time)
            now = datetime.now(tz)
            if now.hour == 8:  # Adjust to your desired time
                send_email(subscriber)

        except Exception as e:
            print(f'Error processing subscriber {subscriber["email"]}: {str(e)}')

# Main program
if __name__ == '__main__':
    send_promotional_emails()