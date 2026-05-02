"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_000.txt
Run      : 1
"""

from flask import Flask, request, session, redirect, render_template_string
from twilio.rest import Client
import random
import os

app = Flask(__name__)
app.secret_key = os.environ['SUPER_SECRET_KEY']  # Replace with a strong secret key

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_verification_code(phone_number, code):
    # Send verification code via SMS using Twilio API
    message = client.messages.create(
        body=f'Your verification code is {code}.',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone']
        code = random.randint(100000, 999999)
        session['verification_code'] = str(code)
        session['phone_number'] = phone_number
        
        try:
            send_verification_code(phone_number, code)
        except Exception as e:
            return f"Failed to send verification code: {str(e)}"
        
        return redirect('/verify')
    
    return render_template_string('''
        <form method="post">
            Phone Number: <input type="text" name="phone">
            <input type="submit" value="Send Code">
        </form>
    ''')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        code_entered = request.form['code']
        if 'verification_code' in session and session['verification_code'] == code_entered:
            return "Access granted!"
        else:
            return "Invalid verification code!"
    
    return render_template_string('''
        <form method="post">
            Verification Code: <input type="text" name="code">
            <input type="submit" value="Verify">
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)