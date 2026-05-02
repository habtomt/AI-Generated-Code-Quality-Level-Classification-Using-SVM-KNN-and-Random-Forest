"""
Auto-generated Python code
Scenario : Web Hosting & Deployment
Prompt   : response_000.txt
Run      : 3
"""

# Import required libraries
import os
import git
import shutil
import paramiko
import yaml

# Load configuration from YAML file
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config.yaml file not found.")
    exit()

# Define constants
REPO_URL = config['repo_url']
REPO_USERNAME = config['repo_username']
REPO_PASSWORD = config['repo_password']
WEBSITE_FOLDER = config['website_folder']
DEPLOYMENT_SERVER = config['deployment_server']
DEPLOYMENT_USERNAME = config['deployment_username']
DEPLOYMENT_PASSWORD = config['deployment_password']
STATIC_FILES_FOLDER = config['static_files_folder']

# Create a temporary directory for static files
try:
    os.mkdir('temp')
except FileExistsError:
    print("Temporary directory already exists.")

# Copy static files to temporary directory
try:
    shutil.copytree(STATIC_FILES_FOLDER, 'temp')
except FileNotFoundError:
    print("Error: static_files_folder not found.")
    exit()

# Initialize Git repository
try:
    repo = git.Repo.init('temp')
except git.exc.InvalidGitRepositoryError:
    print("Error: temporary directory is not a Git repository.")
    exit()

# Add all files to Git repository
repo.git.add('.')

# Commit changes with a default message
repo.git.commit('-m', 'Initial commit')

# Push changes to remote repository
try:
    repo.remotes.origin.push()
except git.exc.NoSuchRemoteError:
    print("Error: remote repository not found.")
    exit()

# Connect to deployment server using SSH
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=DEPLOYMENT_SERVER, username=DEPLOYMENT_USERNAME, password=DEPLOYMENT_PASSWORD)
except paramiko.AuthenticationException:
    print("Error: invalid deployment credentials.")
    exit()

# Upload static files to deployment server
try:
    sftp = ssh.open_sftp()
    for root, dirs, files in os.walk('temp'):
        for file in files:
            remote_path = os.path.join(WEBSITE_FOLDER, os.path.relpath(root, 'temp'), file)
            sftp.put(os.path.join(root, file), remote_path)
    sftp.close()
except Exception as e:
    print("Error:", str(e))

# Configure web server to serve static content
try:
    # Assuming Nginx web server
    with open('/etc/nginx/sites-available/default', 'r') as f:
        nginx_config = f.read()
    nginx_config = nginx_config.replace('your_website_folder', WEBSITE_FOLDER)
    with open('/etc/nginx/sites-available/default', 'w') as f:
        f.write(nginx_config)
    ssh.exec_command('service nginx reload')
except Exception as e:
    print("Error:", str(e))

# Close SSH connection
ssh.close()