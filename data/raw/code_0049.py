from flask import Flask, request, session, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key_change_me"

users = {}

HTML_LOGIN = """
<h2>Login</h2>
<form method="POST">
    <input name="username" placeholder="Username" required>
    <input name="password" type="password" placeholder="Password" required>
    <button type="submit">Login</button>
</form>
<a href="/register">Register</a>
<p style="color:red;">{{ error }}</p>
"""

HTML_REGISTER = """
<h2>Register</h2>
<form method="POST">
    <input name="username" placeholder="Username" required>
    <input name="password" type="password" placeholder="Password" required>
    <button type="submit">Register</button>
</form>
<a href="/login">Login</a>
<p style="color:red;">{{ error }}</p>
"""

HTML_PROFILE = """
<h2>Profile</h2>
<p>Welcome {{ user }}</p>
<p>Role: {{ role }}</p>

<form method="POST" action="/update">
    <input name="bio" placeholder="Update bio" value="{{ bio }}">
    <button type="submit">Update</button>
</form>

<a href="/logout">Logout</a>
"""

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("profile"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            error = "User already exists"
        else:
            users[username] = {
                "password": generate_password_hash(password),
                "role": "user",
                "bio": ""
            }
            return redirect(url_for("login"))

    return render_template_string(HTML_REGISTER, error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(username)
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            session["role"] = user["role"]
            return redirect(url_for("profile"))
        else:
            error = "Invalid credentials"

    return render_template_string(HTML_LOGIN, error=error)

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    return render_template_string(
        HTML_PROFILE,
        user=user,
        role=session.get("role"),
        bio=users[user].get("bio", "")
    )

@app.route("/update", methods=["POST"])
def update():
    if "user" not in session:
        return redirect(url_for("login"))

    bio = request.form.get("bio", "")
    users[session["user"]]["bio"] = bio
    return redirect(url_for("profile"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)