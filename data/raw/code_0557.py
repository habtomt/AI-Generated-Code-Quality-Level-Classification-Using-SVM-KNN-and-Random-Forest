"""
Auto-generated Python code
Scenario : Push Notifications
Prompt   : response_001.txt
Run      : 1
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Email configuration
smtp_server = 'smtp.example.com'  # Replace with your SMTP server
smtp_port = 587  # Port for starttls
smtp_user = 'your_email@example.com'  # Your SMTP username
smtp_password = 'your_password'  # Your SMTP password

# Create a list of recipients
recipients = ['user1@example.com', 'user2@example.com']  # Replace with recipient emails

# Email content
subject = 'New Version of Our App is Now Available!'
body = '''\
Hello,

We're excited to announce that a new version of our app has been released. This update includes several improvements and bug fixes to enhance your experience.

Key updates:
- Performance improvements
- New features added
- Bug fixes

We hope you enjoy the updates. Please let us know if you have any feedback.

Best regards,
Your App Team
'''

def send_emails(smtp_server, smtp_port, smtp_user, smtp_password, recipients, subject, body):
    # Setup SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach a changelog file
    filename = 'changelog.txt'
    if os.path.exists(filename):
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        msg.attach(part)

    for recipient in recipients:
        msg['To'] = recipient
        try:
            # Send the email
            server.sendmail(smtp_user, recipient, msg.as_string())
            print(f'Email sent to {recipient}')
        except Exception as e:
            print(f'Failed to send email to {recipient}: {e}')
    
    # Disconnect from the server
    server.quit()

# Send the emails
send_emails(smtp_server, smtp_port, smtp_user, smtp_password, recipients, subject, body)