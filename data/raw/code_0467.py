"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import os
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import json

# Set up Google Cloud Storage credentials
GCS_CREDENTIALS = {
    "type": "service_account",
    "project_id": "YOUR_PROJECT_ID",
    "private_key_id": "YOUR_PRIVATE_KEY_ID",
    "private_key": "YOUR_PRIVATE_KEY",
    "client_email": "YOUR_CLIENT_EMAIL",
    "client_id": "YOUR_CLIENT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/YOUR_SERVICE_ACCOUNT"
}

# Function to upload a file to Google Cloud Storage
def upload_file_to_gcs(file_path, bucket_name, file_name):
    try:
        # Create a credentials object
        credentials = service_account.Credentials.from_service_account_info(GCS_CREDENTIALS)
        
        # Create a client object
        storage_client = build('storage', 'v1', credentials=credentials)
        
        # Upload the file
        file_body = {'name': file_name}
        media = storage_client.media_upload(
            body=file_body,
            media_body=os.path.join(file_path, file_name),
            chunk_size=10 * 1024 * 1024  # 10MB chunk size
        )
        
        # Wait for the upload to complete
        media.result()
        
        print(f"File uploaded successfully: {file_name}")
        
    except HttpError as e:
        print(f"Error uploading file: {e}")
    
# Function to download a file from Google Cloud Storage
def download_file_from_gcs(bucket_name, file_name):
    try:
        # Create a credentials object
        credentials = service_account.Credentials.from_service_account_info(GCS_CREDENTIALS)
        
        # Create a client object
        storage_client = build('storage', 'v1', credentials=credentials)
        
        # Download the file
        blob = storage_client.objects().get(bucket=bucket_name, object=file_name).execute()
        file_data = requests.get(f"https://storage.googleapis.com/{bucket_name}/{file_name}").content
        
        # Save the file
        with open(file_name, 'wb') as f:
            f.write(file_data)
        
        print(f"File downloaded successfully: {file_name}")
        
    except HttpError as e:
        print(f"Error downloading file: {e}")
    
# Function to manage metadata in Google Cloud Storage
def manage_metadata(bucket_name, file_name, metadata):
    try:
        # Create a credentials object
        credentials = service_account.Credentials.from_service_account_info(GCS_CREDENTIALS)
        
        # Create a client object
        storage_client = build('storage', 'v1', credentials=credentials)
        
        # Update the metadata
        storage_client.objects().update(
            bucket=bucket_name,
            object=file_name,
            body={'name': file_name, **metadata}
        ).execute()
        
        print(f"Metadata updated successfully: {file_name}")
        
    except HttpError as e:
        print(f"Error updating metadata: {e}")

# Usage example
if __name__ == "__main__":
    # Set up the credentials
    with open('credentials.json', 'w') as f:
        json.dump(GCS_CREDENTIALS, f)
    
    # Set up the bucket and file names
    bucket_name = 'your-bucket-name'
    file_name = 'your-file-name.txt'
    
    # Upload a file
    upload_file_to_gcs('/path/to/file', bucket_name, file_name)
    
    # Download a file
    download_file_from_gcs(bucket_name, file_name)
    
    # Manage metadata
    metadata = {'customMetadata': 'custom value'}
    manage_metadata(bucket_name, file_name, metadata)