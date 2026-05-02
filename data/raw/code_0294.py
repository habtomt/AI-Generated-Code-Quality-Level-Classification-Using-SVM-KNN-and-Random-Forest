"""
Auto-generated Python code
Scenario : Authentication & Identity Management
Prompt   : response_002.txt
Run      : 1
"""

from flask import Flask, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)

# Configure the app
app.secret_key = "supersekrit"  # Make sure to change this!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # or your preferred database

# Initialize the database
db = SQLAlchemy(app)

# Define a user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(256), nullable=False)

# Register the OAuth blueprint
google_bp = make_google_blueprint(client_id="YOUR_GOOGLE_CLIENT_ID", 
                                   client_secret="YOUR_GOOGLE_CLIENT_SECRET", 
                                   redirect_to="google_login")
app.register_blueprint(google_bp, url_prefix="/login")

db.create_all()

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        user_info = resp.json()
        user = User.query.filter_by(google_id=user_info["id"]).first()
        if not user:
            user = User(google_id=user_info["id"], username=user_info["name"])
            db.session.add(user)
            db.session.commit()
        return f"Hello, {user.username}!"
    except Exception as e:
        return str(e)

@app.route("/logout")
def logout():
    try:
        token = google_bp.token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"content-type": "application/x-www-form-urlencoded"}
        )
        del google_bp.token  # Forget OAuth token
        session.clear()
        return redirect(url_for("index"))
    except Exception as e:
        return str(e)

@app.route("/login/google")
def google_login():
    return redirect(url_for("google.login"))

if __name__ == "__main__":
    app.run(debug=True)