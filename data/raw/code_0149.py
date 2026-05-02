import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Simulated OAuth 2.0 Flow for a Junior Developer Learning
# Using Mock endpoints to demonstrate the logic of social login

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        query_components = parse_qs(urlparse(self.path).query)
        if 'code' in query_components:
            auth_code = query_components['code'][0]
            # Mock retrieving profile info after getting the code
            user_profile = {
                "id": "12345",
                "name": "John Doe",
                "email": "john.doe@socialmail.com",
                "provider": "MockSocialPlatform"
            }
            
            html = f"""
            <html>
                <body style="font-family: Arial; text-align: center; padding-top: 50px;">
                    <h1 style="color: #2d89ef;">Authentication Successful!</h1>
                    <p>Welcome, <b>{user_profile['name']}</b></p>
                    <div style="background: #f4f4f4; display: inline-block; padding: 20px; border-radius: 8px;">
                        <p align="left"><b>Profile Data Stored:</b></p>
                        <pre align="left">{json.dumps(user_profile, indent=4)}</pre>
                    </div>
                    <p><i>You can close this tab now and check the terminal.</i></p>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
            print(f"\n[OAuth] Code received: {auth_code}")
            print(f"[Database] Storing record: {user_profile['email']} via {user_profile['provider']}")
        else:
            self.wfile.write(b"No code found.")

def start_social_login():
    # Configuration
    CLIENT_ID = "your_social_app_client_id"
    REDIRECT_URI = "http://localhost:8080/callback"
    AUTH_URL = "https://mock-social-platform.com/oauth/authorize"
    
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "profile email"
    }
    
    login_url = f"{AUTH_URL}?{urlencode(params)}"
    
    print("--- Social Media Login (OAuth 2.0) ---")
    print(f"Directing user to: {AUTH_URL}")
    print("1. Mock Platform Authorization")
    print("2. Callback to local server")
    
    # In a real scenario, this opens the browser. 
    # Here we simulate the redirect to our local server to show the flow.
    simulated_callback = f"{REDIRECT_URI}?code=MOCK_AUTH_CODE_XYZ_123"
    
    print(f"\nOpening browser for login simulation...")
    # Since we can't actually open a remote social site, we trigger our callback directly
    webbrowser.open(simulated_callback)

if __name__ == "__main__":
    # Start a local server to handle the OAuth callback
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, OAuthHandler)
    
    print("Local Auth Server started at http://localhost:8080")
    print("Simulating OAuth redirection...")
    
    start_social_login()
    
    # Handle one request then exit
    httpd.handle_request()