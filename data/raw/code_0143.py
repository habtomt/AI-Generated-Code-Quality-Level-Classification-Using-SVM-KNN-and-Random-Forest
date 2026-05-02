#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

REPO_URL = os.getenv("REPO_URL", "https://github.com/yourusername/yourrepo.git")
BRANCH = "main"

PROJECT_DIR = Path.cwd()
WORKFLOW_DIR = PROJECT_DIR / ".github" / "workflows"
NGINX_DIR = PROJECT_DIR / "deployment"

def run(cmd):
    subprocess.run(cmd, check=True, shell=True)

def init_git():
    if not (PROJECT_DIR / ".git").exists():
        run("git init")
        run(f"git branch -M {BRANCH}")
    run("git add .")
    run('git commit -m "Initial commit: static site deployment setup" || echo "No changes to commit"')
    run(f"git remote add origin {REPO_URL} || true")
    run(f"git push -u origin {BRANCH} || true")

def create_github_actions():
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
    workflow_file = WORKFLOW_DIR / "deploy.yml"

    workflow_content = f"""
name: Deploy Static Site

on:
  push:
    branches: [{BRANCH}]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Deploy to server via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{{{ secrets.SERVER_HOST }}}}
          username: ${{{{ secrets.SERVER_USER }}}}
          key: ${{{{ secrets.SERVER_SSH_KEY }}}}
          script: |
            cd /var/www/html
            git pull origin {BRANCH}
            sudo systemctl restart nginx
"""

    workflow_file.write_text(workflow_content.strip())

def create_nginx_config():
    NGINX_DIR.mkdir(exist_ok=True)

    config = """
server {
    listen 80;
    server_name your_domain_or_ip;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
"""
    (NGINX_DIR / "nginx.conf").write_text(config.strip())

def main():
    create_github_actions()
    create_nginx_config()
    init_git()

if __name__ == "__main__":
    main()