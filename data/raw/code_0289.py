import os
import subprocess

# --- Configuration ---
REPO_PATH = "./my_static_site"
REMOTE_URL = "https://github.com/username/repository.git"
WEB_SERVER_CONFIG_PATH = "/etc/nginx/sites-available/default"
STATIC_FILES_DIR = os.path.abspath(REPO_PATH)

def setup_git_and_push():
    """Initializes git and pushes to a remote repository."""
    os.makedirs(REPO_PATH, exist_ok=True)
    with open(os.path.join(REPO_PATH, "index.html"), "w") as f:
        f.write("<html><body><h1>Hello World</h1></body></html>")

    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit"],
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", REMOTE_URL],
        ["git", "push", "-u", "origin", "main"]
    ]

    for cmd in commands:
        subprocess.run(cmd, cwd=REPO_PATH)

def configure_web_server():
    """Configures Nginx to serve static files."""
    nginx_config = f"""
server {{
    listen 80;
    server_name localhost;

    location / {{
        root {STATIC_FILES_DIR};
        index index.html;
    }}
}}
"""
    # Requires sudo privileges to write to system config
    with open("nginx_site_config", "w") as f:
        f.write(nginx_config)
    
    print("Nginx configuration generated in 'nginx_site_config'.")
    print(f"To apply, move to {WEB_SERVER_CONFIG_PATH} and restart Nginx.")

def ci_cd_pipeline_mock():
    """Simulates a CD pipeline trigger."""
    print("Triggering CD Pipeline...")
    print(f"Pulling latest changes from {REMOTE_URL}...")
    subprocess.run(["git", "pull", "origin", "main"], cwd=REPO_PATH)
    print("Deploying static assets to web server root...")
    subprocess.run(["sudo", "systemctl", "reload", "nginx"])

if __name__ == "__main__":
    setup_git_and_push()
    configure_web_server()
    ci_cd_pipeline_mock()