"""
Auto-generated Python code
Scenario : Web Hosting & Deployment
Prompt   : response_000.txt
Run      : 1
"""

import os
import yaml
import paramiko
import ssh2

# Prerequisites
# Git installed on your local machine
# A GitHub account (or similar Git-based repository service like GitLab/Bitbucket)
# A server with SSH access and an installed Nginx web server
# Continuous deployment service such as GitHub Actions

# Initialize a Git Repository
def init_git_repo():
    # Create Your Static Website Files
    with open('index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Static Site</title>
</head>
<body>
    <h1>Welcome to My Static Website!</h1>
    <p>This site is served using a continuous deployment pipeline.</p>
</body>
</html>''')

    # Initialize a Git repository:
    os.system('git init')
    os.system('git add .')
    os.system('git commit -m "Initial commit"')

    # Push to GitHub:
    os.system('git remote add origin https://github.com/your-username/your-repo-name.git')
    os.system('git branch -M main')
    os.system('git push -u origin main')

# Set Up Continuous Deployment with GitHub Actions
def deploy_static_files():
    # Create a GitHub Actions Workflow:
    with open('deploy.yml', 'w') as f:
        workflow = '''name: Deploy to Server

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Copy files via SSH
      uses: appleboy/scp-action@v0.1.8
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_KEY }}
        source: "src" # Replace with the path to static files, if necessary
        target: "/var/www/html" # Directory on the server
'''
        f.write(yaml.dump(yaml.safe_load(workflow), default_flow_style=False))

# Configure Secrets in GitHub
def configure_secrets():
    # Configure Secrets in GitHub:
    secrets = ['SERVER_HOST', 'SERVER_USER', 'SERVER_KEY']
    for secret in secrets:
        os.system(f'echo {secret} > .github/secrets/{secret}')

# Configure Nginx to Serve Static Content
def configure_nginx():
    # SSH into your server:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('your-server-ip', username='your-username', key_filename='your-private-key')

    # Install Nginx:
    ssh_client.exec_command('sudo apt update')
    ssh_client.exec_command('sudo apt install nginx')

    # Configure Nginx:
    nginx_config = '''server {
        listen 80;
        listen [::]:80;

        root /var/www/html;
        index index.html;

        server_name your-domain.com;  # Substitute your domain or server IP

        location / {
            try_files $uri $uri/ =404;
        }
    }'''
    ssh_client.exec_command(f'sudo nano /etc/nginx/sites-available/default')
    stdin, stdout, stderr = ssh_client.exec_command(f'echo {nginx_config} >> /etc/nginx/sites-available/default')
    ssh_client.exec_command('sudo systemctl restart nginx')

    ssh_client.close()

# Main program
if __name__ == '__main__':
    init_git_repo()
    deploy_static_files()
    configure_secrets()
    configure_nginx()