from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key'

users_db = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    users_db[username] = generate_password_hash(password)
    return "User registered"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users_db and check_password_hash(users_db[username], password):
        session['user'] = username
        return f"Logged in as {username}"
    return "Login failed", 401

@app.route('/profile')
def profile():
    if 'user' in session:
        return f"Welcome {session['user']}"
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)