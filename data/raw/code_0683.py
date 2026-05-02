"""
Auto-generated Python code
Scenario : Video Streaming & Hosting
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
from flask_uploads import UploadNotAllowed
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz
from PIL import Image

# Create a new Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'static', 'photos')
app.config['UPLOADED_DOCUMENTS_DEST'] = os.path.join(os.getcwd(), 'static', 'documents')

# Configure Flask-SQLAlchemy
db = SQLAlchemy(app)

# Configure Flask-Uploads
photos = UploadSet('photos', IMAGES)
documents = UploadSet('documents', DOCUMENTS)
configure_uploads(app, photos)
configure_uploads(app, documents)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(128), nullable=True)
    documents = db.relationship('Document', backref='author', lazy=True)
    videos = db.relationship('Video', backref='author', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define Video model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    video_file = db.Column(db.String(128), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.utc))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define Document model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    document_file = db.Column(db.String(128), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.utc))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define registration form
class RegistrationForm(FlaskForm):
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(128), nullable=True)

# Define login form
class LoginForm(FlaskForm):
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Define video upload form
class VideoUploadForm(FlaskForm):
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    video_file = db.Column(db.String(128), nullable=False)

# Define document upload form
class DocumentUploadForm(FlaskForm):
    name = db.Column(db.String(128), nullable=False)
    document_file = db.Column(db.String(128), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Define routes
@app.route('/')
def index():
    return 'Welcome to the video sharing platform!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return 'User created successfully!'
    return 'Invalid form submission.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return 'User logged in successfully!'
        return 'Invalid username or password.'
    return 'Invalid form submission.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'User logged out successfully!'

@app.route('/upload/video', methods=['GET', 'POST'])
@login_required
def upload_video():
    form = VideoUploadForm()
    if form.validate_on_submit():
        file = photos.save(request.files['video_file'])
        video = Video(title=form.title.data, description=form.description.data, video_file=file, author=current_user)
        db.session.add(video)
        db.session.commit()
        return 'Video uploaded successfully!'
    return 'Invalid form submission.'

@app.route('/upload/document', methods=['GET', 'POST'])
@login_required
def upload_document():
    form = DocumentUploadForm()
    if form.validate_on_submit():
        file = documents.save(request.files['document_file'])
        document = Document(name=form.name.data, document_file=file, author=current_user)
        db.session.add(document)
        db.session.commit()
        return 'Document uploaded successfully!'
    return 'Invalid form submission.'

@app.errorhandler(404)
def not_found(error):
    return 'Page not found.', 404

if __name__ == '__main__':
    app.run(debug=True)