"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import pytz
from datetime import timedelta

# Set placeholder credentials (replace with actual credentials)
YOUR_API_KEY = "YOUR_API_KEY"
YOUR_API_SECRET = "YOUR_API_SECRET"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "your-email@gmail.com"
PASSWORD = "your-password"

# Set up email content template
email_content = """
Subject: Exclusive Offer for You!

Dear {name},

We hope this email finds you well in your {time_zone} timezone. As a valued customer, we're excited to offer you an exclusive deal that you won't want to miss!

Enjoy 15% off our best-selling products for the next 24 hours. Simply use the code {coupon_code} at checkout to redeem your discount.

Don't miss out on this amazing opportunity to elevate your style and save big. Shop now and experience the difference for yourself!

Best regards,
[Your Name]
"""

# Set up email sender function
def send_email(to_email, name, time_zone, coupon_code):
    # Create message container - the correct MIME type is multipart/alternative
    msg = MIMEMultipart('alternative')
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Exclusive Offer for You!"

    # Create the body of the message (a plain text and an HTML version)
    text = f"Dear {name},\n\nWe hope this email finds you well in your {time_zone} timezone.\n\nBest regards,\n[Your Name]"
    html = email_content.format(name=name, time_zone=time_zone, coupon_code=coupon_code)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send the email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)
    server.sendmail(FROM_EMAIL, to_email, msg.as_string())
    server.quit()

# Set up API connection to retrieve customer data
import requests
data = requests.get(f'https://api.example.com/customers', headers={'Authorization': f'Bearer {YOUR_API_KEY}'}).json()

# Set up timezone information
time_zone_data = {
    'America/New_York': 'EST',
    'America/Los_Angeles': 'PST',
    'Europe/London': 'GMT',
    'Australia/Sydney': 'AEDT'
}

# Set up timezone dictionary
time_zones = {
    customer['id']: time_zone_data[customer['timezone']]
    for customer in data['customers']
}

# Set up coupon code dictionary
coupon_codes = {
    customer['id']: f'CUSTOMER-{customer["id"]}-COUPON'
    for customer in data['customers']
}

# Set up email sender loop
for customer in data['customers']:
    try:
        # Get current time in customer's timezone
        time_zone = time_zones[customer['id']]
        tz = pytz.timezone(time_zone)
        current_time = datetime.datetime.now(tz)
        next_24_hours = current_time + timedelta(hours=24)

        # Check if it's within the time frame to send the email
        if current_time < next_24_hours:
            send_email(customer['email'], customer['name'], time_zone, coupon_codes[customer['id']])
            print(f"Email sent to {customer['email']}")

    except Exception as e:
        print(f"Error sending email to {customer['email']}: {str(e)}")