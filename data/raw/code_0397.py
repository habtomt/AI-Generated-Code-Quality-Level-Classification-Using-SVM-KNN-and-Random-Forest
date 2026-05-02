"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_000.txt
Run      : 1
"""

import boto3
import os
from botocore.exceptions import NoCredentialsError
import schedule
import time

# Configure your AWS credentials and S3 bucket name
AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'
BUCKET_NAME = 'your_s3_bucket_name'
LOCAL_BACKUP_DIR = '/path/to/local/directory/to/backup'

# Initialize Boto3 S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_KEY)

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket."""
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f"{file_name} has been uploaded to {bucket}.")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

def backup_files():
    """Backup files from a local directory to the S3 bucket."""
    for root, dirs, files in os.walk(LOCAL_BACKUP_DIR):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, LOCAL_BACKUP_DIR)
            s3_path = relative_path.replace("\\", "/")  # Ensure path format for S3 keys

            upload_to_s3(local_path, BUCKET_NAME, s3_path)

# Schedule the backup to run at a specific interval - for example, daily
schedule.every().day.at("01:00").do(backup_files)  # Runs daily at 01:00 AM

# Run scheduled tasks
while True:
    try:
        schedule.run_pending()
        time.sleep(60)  # Wait for one minute
    except KeyboardInterrupt:
        print("Backup script stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")