"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_003.txt
Run      : 1
"""

# Import necessary libraries
from flask import Flask, request, render_template_string, send_file
from flask_mail import Mail, Message
import logging

# Create a Flask application
app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'YOUR_EMAIL@gmail.com'
app.config['MAIL_PASSWORD'] = 'YOUR_EMAIL_PASSWORD'

# Initialize Flask-Mail
mail = Mail(app)

# Initialize a simple in-memory list to store subscribers
subscribers = []

# Define the HTML template for the subscription form
subscription_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Newsletter Subscription</title>
</head>
<body>
  <h1>Subscribe to our Newsletter</h1>
  <form action="/subscribe" method="POST">
    <input type="email" name="email" required placeholder="Enter your email" />
    <button type="submit">Subscribe</button>
  </form>
</body>
</html>
'''

# Define the HTML template for the manage preferences page
manage_html = '''
<h1>Manage Preferences</h1>
<p>Your email: {{ email }}</p>
<button onclick="unsubscribe()">Unsubscribe</button>
<script>
  function unsubscribe() {
    fetch('/unsubscribe?email={{ email | urlencode }}', { method: 'POST' })
      .then(response => response.text())
      .then(data => alert(data))
      .catch(error => console.error('Error:', error));
  }
</script>
'''

# Route to serve the subscription form
@app.route('/', methods=['GET'])
def index():
    return render_template_string(subscription_html)

# Route to handle subscription form submission
@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        email = request.form['email']
        if email not in subscribers:
            subscribers.append(email)
            # Send a confirmation email
            msg = Message("Thanks for subscribing!", sender="YOUR_EMAIL@gmail.com", recipients=[email])
            msg.body = f"You have subscribed to our newsletter. Manage your preferences here: http://localhost:5000/manage?email={email}"
            mail.send(msg)
            return 'Subscription successful, confirmation email sent'
        else:
            return 'This email is already subscribed'
    except Exception as e:
        logging.error(f"Error: {e}")
        return 'Error subscribing'

# Route to manage subscription preferences
@app.route('/manage', methods=['GET'])
def manage():
    try:
        email = request.args.get('email')
        if email in subscribers:
            return render_template_string(manage_html, email=email)
        else:
            return 'Email not found'
    except Exception as e:
        logging.error(f"Error: {e}")
        return 'Error managing preferences'

# Route to handle unsubscribe
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    try:
        email = request.args.get('email')
        subscribers.remove(email)
        return 'Successfully unsubscribed'
    except Exception as e:
        logging.error(f"Error: {e}")
        return 'Error unsubscribing'

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)