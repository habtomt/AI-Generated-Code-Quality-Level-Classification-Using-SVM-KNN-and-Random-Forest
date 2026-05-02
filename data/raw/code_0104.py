from flask import Flask, redirect, request, session, url_for, jsonify
import requests
import os
import secrets

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret_key")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/callback/google")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@app.route("/")
def home():
    return """
    <h2>Social Login Demo</h2>
    <a href="/login/google">Login with Google</a>
    """


@app.route("/login/google")
def login_google():
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }

    url = AUTH_URL + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    return redirect(url)


@app.route("/callback/google")
def callback_google():
    error = request.args.get("error")
    if error:
        return jsonify({"error": error})

    state = request.args.get("state")
    if state != session.get("oauth_state"):
        return jsonify({"error": "Invalid state"}), 400

    code = request.args.get("code")

    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()

    access_token = token_json.get("access_token")

    if not access_token:
        return jsonify(token_json), 400

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(USERINFO_URL, headers=headers)
    userinfo = userinfo_response.json()

    user = upsert_user(userinfo)

    return jsonify({
        "message": "Login successful",
        "user": user
    })


def upsert_user(userinfo):
    user_db = session.get("user_db", {})

    email = userinfo.get("email")
    if email in user_db:
        user_db[email].update(userinfo)
    else:
        user_db[email] = userinfo

    session["user_db"] = user_db
    return user_db[email]


if __name__ == "__main__":
    app.run(debug=True)