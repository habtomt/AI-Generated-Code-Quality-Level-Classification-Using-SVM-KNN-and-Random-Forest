"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_001.txt
Run      : 1
"""

from flask import Flask, request, render_template_string, session, redirect, url_for
import pyotp
import qrcode
import io
from base64 import b64encode

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# You would retrieve this from your database
users = {
    "user@example.com": {
        "password": "securepassword",  # This should be hashed in a real app
        "otp_secret": pyotp.random_base32()
    }
}

@app.route('/')
def home():
    return 'Welcome to the MFA demo! Go to /login to start.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = users.get(email)
            
            if user and user['password'] == password:
                session['email'] = email
                return redirect(url_for('mfa'))
            else:
                return 'Invalid email or password'
        except Exception as e:
            return str(e)
    
    return '''
        <form method="post">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))
    
    user = users.get(email)
    otp_secret = user['otp_secret']
    
    if request.method == 'POST':
        try:
            otp_token = request.form['otp']
            totp = pyotp.TOTP(otp_secret)
            if totp.verify(otp_token):
                return 'Authenticated successfully!'
            else:
                return 'Invalid OTP'
        except Exception as e:
            return str(e)

    # Generate QR code
    totp = pyotp.TOTP(otp_secret)
    otp_uri = totp.provisioning_uri(name=email, issuer_name="Your App Name")
    qr = qrcode.make(otp_uri)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    qr_code = b64encode(buf.getvalue()).decode('utf-8')

    return render_template_string('''
        <h1>MFA Required</h1>
        <img src="data:image/png;base64,{{qr_code}}" alt="QR Code">
        <p>Scan this QR code with your authenticator app.</p>
        <form method="post">
            Enter the OTP from your app: <input type="text" name="otp"><br>
            <input type="submit" value="Verify">
        </form>
    ''', qr_code=qr_code)

if __name__ == '__main__':
    app.run(debug=True)