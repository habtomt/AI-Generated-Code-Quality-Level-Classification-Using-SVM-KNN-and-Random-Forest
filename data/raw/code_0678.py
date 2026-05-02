"""
Auto-generated Python code
Scenario : Video Streaming & Hosting
Prompt   : response_002.txt
Run      : 1
"""

# Importing necessary libraries
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from bson import ObjectId

# Creating a new Flask application
app = Flask(__name__)

# Enabling CORS
CORS(app)

# Configuring the MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/video-sharing-platform'
db = MongoEngine(app)

# Defining a User model
class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    def save(self, *args, **kwargs):
        self.password = generate_password_hash(self.password)
        super(User, self).save(*args, **kwargs)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Defining a Video model
class Video(db.Document):
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    user = db.ReferenceField(User)
    url = db.StringField(required=True)

# Function to generate a JWT
def generate_jwt(user):
    return jwt.encode({'id': str(user.id), 'username': user.username}, 'SECRET_KEY', algorithm='HS256')

# Authentication route
@app.route('/api/auth/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return jsonify({'token': generate_jwt(user).decode('UTF-8')})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404

# Registration route
@app.route('/api/auth/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        user = User.objects.get(email=email)
        return jsonify({'error': 'User already exists'}), 400
    except User.DoesNotExist:
        user = User(username=username, email=email, password=password)
        user.save()
        return jsonify({'message': 'User created successfully'}), 201

# Video upload route
@app.route('/api/videos', methods=['POST'])
def upload_video():
    title = request.json.get('title')
    description = request.json.get('description')
    user_id = request.json.get('user_id')
    
    try:
        user = User.objects.get(id=user_id)
        video = Video(title=title, description=description, user=user, url='VIDEO_URL')
        video.save()
        return jsonify({'message': 'Video uploaded successfully'}), 201
    except (User.DoesNotExist, ValueError):
        return jsonify({'error': 'Invalid user or video data'}), 400

# Report video route
@app.route('/api/moderation/report', methods=['POST'])
def report_video():
    video_id = request.json.get('video_id')
    reason = request.json.get('reason')
    user_id = request.json.get('user_id')

    try:
        user = User.objects.get(id=user_id)
        report = {'video_id': video_id, 'reason': reason, 'user': user_id}
        report_doc = db.Report(**report)
        report_doc.save()
        return jsonify({'message': 'Report submitted successfully'}), 201
    except (User.DoesNotExist, ValueError):
        return jsonify({'error': 'Invalid user or report data'}), 400

# Run the application
if __name__ == '__main__':
    app.run(debug=True)