"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
import os
import datetime
import pickle
import boto3
from botocore.exceptions import NoCredentialsError

# Set AWS credentials
AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'
AWS_BUCKET_NAME = 'YOUR_AWS_BUCKET_NAME'
AWS_REGION_NAME = 'YOUR_AWS_REGION_NAME'

# Initialize AWS S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                     aws_secret_access_key=AWS_SECRET_KEY,
                     region_name=AWS_REGION_NAME)

# Function to create a backup file
def create_backup_file(data):
    # Create a backup file name with current timestamp
    backup_file_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
    
    # Use pickle to serialize the data and store it in the backup file
    with open(backup_file_name, 'wb') as f:
        pickle.dump(data, f)
    
    return backup_file_name

# Function to upload the backup file to AWS S3
def upload_backup_to_s3(backup_file_name):
    try:
        # Upload the backup file to AWS S3
        s3.upload_file(backup_file_name, AWS_BUCKET_NAME, backup_file_name)
        
        # Remove the local backup file
        os.remove(backup_file_name)
        
        print(f"Backup uploaded to AWS S3 successfully.")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to perform regular backups
def regular_backups(data, interval=60):  # default interval is 1 minute
    while True:
        # Create a backup file
        backup_file_name = create_backup_file(data)
        
        # Upload the backup file to AWS S3
        upload_backup_to_s3(backup_file_name)
        
        # Wait for the specified interval
        import time
        time.sleep(interval)

# Example usage
data = {"key": "value"}  # Sample data to backup
regular_backups(data)