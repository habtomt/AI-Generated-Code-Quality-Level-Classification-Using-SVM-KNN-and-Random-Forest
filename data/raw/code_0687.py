"""
Auto-generated Python code
Scenario : Video Streaming & Hosting
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email
from flask_uploads import UploadManager
from cloudinary.uploader import upload
from cloudinary.api import delete_resources_by_tag
from cloudinary import config
from cloudinary.exceptions import ResourceNotFound
import os
import uuid
from youtube_dl import YoutubeDL
from pytube import YouTube

# Create a new Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

# Initialize Flask extensions
db = SQLAlchemy(app)
CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Define the video model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define the video form
class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=['Sports', 'Music', 'Gaming'])

# Initialize the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define a route to upload a video
@app.route('/upload', methods=['POST'])
@login_required
def upload_video():
    try:
        # Create a new upload manager
        upload_manager = UploadManager('uploads')
        
        # Get the video file from the request
        video_file = request.files['video']
        
        # Upload the video to Cloudinary
        video = upload(
            file=video_file,
            public_id=uuid.uuid4().hex,
            resource_type='video',
            overwrite=True
        )
        
        # Get the video URL from Cloudinary
        video_url = video['secure_url']
        
        # Create a new video instance
        new_video = Video(
            title=request.form['title'],
            description=request.form['description'],
            category=request.form['category'],
            user_id=current_user.id
        )
        
        # Add the video to the database
        db.session.add(new_video)
        db.session.commit()
        
        # Return a success message
        return jsonify({'message': 'Video uploaded successfully'})
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'message': str(e)})

# Define a route to view videos
@app.route('/videos', methods=['GET'])
@login_required
def view_videos():
    try:
        # Get all videos from the database
        videos = Video.query.all()
        
        # Return a list of video titles
        return jsonify([video.title for video in videos])
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'message': str(e)})

# Define a route to delete a video
@app.route('/delete/<int:video_id>', methods=['DELETE'])
@login_required
def delete_video(video_id):
    try:
        # Get the video from the database
        video = Video.query.get(video_id)
        
        # If the video exists, delete it from the database and Cloudinary
        if video:
            # Delete the video from the database
            db.session.delete(video)
            db.session.commit()
            
            # Delete the video from Cloudinary
            delete_resources_by_tag(video_url)
            
            # Return a success message
            return jsonify({'message': 'Video deleted successfully'})
        else:
            # Return an error message if the video does not exist
            return jsonify({'message': 'Video not found'})
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'message': str(e)})

# Define a route to categorize a video
@app.route('/categorize/<int:video_id>', methods=['PUT'])
@login_required
def categorize_video(video_id):
    try:
        # Get the video from the database
        video = Video.query.get(video_id)
        
        # If the video exists, update its category
        if video:
            # Update the video's category
            video.category = request.form['category']
            
            # Add the video to the database
            db.session.commit()
            
            # Return a success message
            return jsonify({'message': 'Video categorized successfully'})
        else:
            # Return an error message if the video does not exist
            return jsonify({'message': 'Video not found'})
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'message': str(e)})

# Define a route to login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the username and password from the request
        username = request.form['username']
        password = request.form['password']
        
        # Get the user from the database
        user = User.query.filter_by(username=username, password=password).first()
        
        # If the user exists, login the user
        if user:
            login_user(user)
            return jsonify({'message': 'Logged in successfully'})
        else:
            # Return an error message if the user does not exist
            return jsonify({'message': 'Invalid username or password'})
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'message': str(e)})

# Define a route to logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        # Logout the current user
        logout_user()
        
        # Return a success message
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'message': str(e)})

# Create the database tables
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)