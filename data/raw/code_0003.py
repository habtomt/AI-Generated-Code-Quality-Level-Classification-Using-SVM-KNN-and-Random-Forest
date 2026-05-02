import sqlite3
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import urllib.parse

DB_NAME = "oauth_users.db"

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8000/callback"
AUTH_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"

auth_code = None

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT,
            provider_id TEXT,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/callback":
            query = urllib.parse.parse_qs(parsed_path.query)
            auth_code = query.get("code")[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authentication successful. You can close this window.")

def start_server():
    server = HTTPServer(("localhost", 8000), OAuthHandler)
    server.handle_request()

def get_access_token(code):
    headers = {"Accept": "application/json"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    return response.json().get("access_token")

def get_user_info(token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get(USER_API_URL, headers=headers)
    return response.json()

def save_user(provider, provider_id, username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (provider, provider_id, username) VALUES (?, ?, ?)",
        (provider, provider_id, username)
    )
    conn.commit()
    conn.close()

def oauth_login():
    global auth_code
    auth_code = None

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "read:user"
    }

    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    threading.Thread(target=start_server).start()
    webbrowser.open(url)

    while auth_code is None:
        pass

    token = get_access_token(auth_code)
    user_info = get_user_info(token)

    provider_id = str(user_info.get("id"))
    username = user_info.get("login")

    save_user("github", provider_id, username)

    print(f"Logged in as {username}")

if __name__ == "__main__":
    init_db()

    while True:
        print("\n1. Login with GitHub\n2. Exit")
        choice = input("Select: ")

        if choice == "1":
            oauth_login()
        elif choice == "2":
            break
