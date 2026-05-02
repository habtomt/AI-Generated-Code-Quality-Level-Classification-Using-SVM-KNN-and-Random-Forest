"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_002.txt
Run      : 1
"""

# Import necessary libraries
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Create a new Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///access_management.db'  # replace with your database URI
db = SQLAlchemy(app)

# Define database models for Users, Roles, and Permissions
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.relationship('Permission', backref='role', lazy=True)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

# Create authentication and authorization functions
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        # This is where you validate the token
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        # Create a token (simple way, not secure, for illustration only)
        token = f'token-{user.username}'
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Role-Based Access Control
def check_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role')
            role = Role.query.filter_by(name=user_role).first()
            if not any(p.permission_name == permission for p in role.permissions):
                return jsonify({'message': 'Access denied'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Define routes with role checking
@app.route('/secure-data', methods=['GET'])
@token_required
@check_permission('view_data')
def secure_data():
    return jsonify({'message': 'This is secured data'})

@app.route('/admin', methods=['GET'])
@token_required
@check_permission('admin_access')
def admin_panel():
    return jsonify({'message': 'Welcome to the admin panel'})

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()
    if not Role.query.first():
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()

    if not User.query.first():
        admin_user = User(username='admin', password=generate_password_hash('admin', method='sha256'), role_id=1)
        db.session.add(admin_user)
        db.session.commit()

# Run the application
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")