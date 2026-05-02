"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_001.txt
Run      : 1
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import datetime

# Email configuration
sender_email = "YOUR_EMAIL@gmail.com"
sender_password = "YOUR_PASSWORD"
receiver_email = "RECEIVER_EMAIL@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Email sequence content
email_sequence = [
    {
        "subject": "Welcome to [Your Brand] – Let's Get Started!",
        "content": "Greet the subscriber and express gratitude for subscribing. Briefly introduce your brand and what they can expect from your emails. Provide a welcome offer or incentive, such as a discount code or free resource.",
        "timing": 0  # Immediately after subscription
    },
    {
        "subject": "Discover Our [Products/Services] and How They Can Benefit You",
        "content": "Introduce your main products or services. Highlight the benefits and unique features. Use customer testimonials or success stories if available.",
        "timing": 2  # 2-3 days after the welcome email
    },
    {
        "subject": "Here's How to Make the Most Out of [Product/Service]!",
        "content": "Provide useful tips or educational content that relates to your product/service. Demonstrate how your product/service solves a problem or adds value.",
        "timing": 5  # 3-5 days after the second email
    },
    {
        "subject": "See How Others Are Succeeding with [Your Brand]",
        "content": "Share detailed success stories or case studies of customers who have benefited from your products/services. Include quotes, statistics, and results.",
        "timing": 9  # 4-7 days after the third email
    },
    {
        "subject": "Exclusive Offer Just for You!",
        "content": "Provide a personalized offer or reminder about any welcome discounts. Encourage urgency with a limited-time offer.",
        "timing": 14  # 6-10 days after the fourth email
    },
    {
        "subject": "We Value Your Feedback and Want to Hear from You!",
        "content": "Ask for feedback on the email series and your product/service. Encourage further engagement with social media links, community groups, or webinars.",
        "timing": 17  # 7-10 days after the fifth email
    }
]

def send_email(subject, content, receiver_email):
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "plain"))
        
        # Set up the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email: ", str(e))

def main():
    subscription_time = datetime.datetime.now()
    for email in email_sequence:
        timing = email["timing"]
        subject = email["subject"]
        content = email["content"]
        
        # Calculate the time to send the email
        send_time = subscription_time + datetime.timedelta(days=timing)
        current_time = datetime.datetime.now()
        
        # Wait until it's time to send the email
        while current_time < send_time:
            time.sleep(60)  # Check every minute
            current_time = datetime.datetime.now()
        
        # Send the email
        send_email(subject, content, receiver_email)

if __name__ == "__main__":
    main()