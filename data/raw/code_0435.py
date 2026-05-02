"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_003.txt
Run      : 2
"""

# Importing necessary libraries
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)  # Generate a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Initialize the LoginManager instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if not logged in

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        # Hash the password before storing it
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # Compare the hashed password with the input password
        return check_password_hash(self.password, password)

# Define the UserLoader function for the LoginManager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the routes for the app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return 'Passwords do not match', 400

        user = User.query.filter_by(username=username).first()
        if user:
            return 'Username already exists', 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return 'Invalid username or password', 400

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)