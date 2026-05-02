"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_004.txt
Run      : 1
"""

from flask import Flask, request, redirect, url_for, render_template, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sample user database (normally you would use a real database)
users = {
    'user1': {'password': 'password1', 'role': 'admin'},
    'user2': {'password': 'password2', 'role': 'user'},
    'user3': {'password': 'password3', 'role': 'guest'},
}

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user_role = users[user_id]['role']
        return User(user_id, user_role)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            if username in users and users[username]['password'] == password:
                user = User(username, users[username]['role'])
                login_user(user)
                return redirect(url_for('index'))
            else:
                return "Invalid credentials", 403
        except Exception as e:
            return str(e), 500
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role != role:
                return "Access denied", 403
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@app.route('/')
@login_required
def index():
    return f"Hello, {current_user.id}! Your role is {current_user.role}."

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return "Admin access granted."

@app.route('/user')
@login_required
@role_required('user')
def user_view():
    return "User access granted."

@app.route('/guest')
@login_required
@role_required('guest')
def guest():
    return "Guest access granted."

if __name__ == '__main__':
    app.run(debug=True)

# Create a template for login (login.html)
# This will be created as a separate file, not part of the python script