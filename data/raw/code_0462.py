"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_000.txt
Run      : 2
"""

# Import required libraries
import os
import boto3
from botocore.exceptions import NoCredentialsError

# Define AWS credentials
AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_ACCESS_KEY'
AWS_BUCKET_NAME = 'YOUR_BUCKET_NAME'

# Initialize AWS S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_file_to_s3(file_path, file_name):
    """
    Uploads a file to AWS S3 bucket.
    
    Args:
    file_path (str): Path to the file to upload.
    file_name (str): Name of the file to upload.
    
    Returns:
    bool: True if file uploaded successfully, False otherwise.
    """
    try:
        # Upload file to S3
        s3_client.upload_file(file_path, AWS_BUCKET_NAME, file_name)
        return True
    except FileNotFoundError:
        # Handle file not found error
        print("The file was not found.")
        return False
    except NoCredentialsError:
        # Handle AWS credentials error
        print("Credentials not available.")
        return False

def download_file_from_s3(file_name):
    """
    Downloads a file from AWS S3 bucket.
    
    Args:
    file_name (str): Name of the file to download.
    
    Returns:
    bool: True if file downloaded successfully, False otherwise.
    """
    try:
        # Download file from S3
        s3_client.download_file(AWS_BUCKET_NAME, file_name, file_name)
        return True
    except NoCredentialsError:
        # Handle AWS credentials error
        print("Credentials not available.")
        return False

def list_files_in_s3():
    """
    Lists all files in the AWS S3 bucket.
    
    Returns:
    list: List of files in the S3 bucket.
    """
    try:
        # List files in S3
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        return [obj['Key'] for obj in response['Contents']]
    except NoCredentialsError:
        # Handle AWS credentials error
        print("Credentials not available.")
        return []

def delete_file_from_s3(file_name):
    """
    Deletes a file from the AWS S3 bucket.
    
    Args:
    file_name (str): Name of the file to delete.
    
    Returns:
    bool: True if file deleted successfully, False otherwise.
    """
    try:
        # Delete file from S3
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_name)
        return True
    except NoCredentialsError:
        # Handle AWS credentials error
        print("Credentials not available.")
        return False

def update_file_metadata(file_name, metadata):
    """
    Updates the metadata of a file in the AWS S3 bucket.
    
    Args:
    file_name (str): Name of the file to update metadata for.
    metadata (dict): Dictionary containing metadata to update.
    
    Returns:
    bool: True if metadata updated successfully, False otherwise.
    """
    try:
        # Update file metadata in S3
        s3_client.put_object_acl(Bucket=AWS_BUCKET_NAME, Key=file_name, ACL='public-read')
        return True
    except NoCredentialsError:
        # Handle AWS credentials error
        print("Credentials not available.")
        return False

# Example usage
if __name__ == "__main__":
    # Upload a file to S3
    print(upload_file_to_s3('path/to/your/file.txt', 'file.txt'))

    # List all files in the S3 bucket
    print(list_files_in_s3())

    # Download a file from S3
    print(download_file_from_s3('file.txt'))

    # Delete a file from S3
    print(delete_file_from_s3('file.txt'))

    # Update file metadata
    metadata = {'ContentType': 'text/plain'}
    print(update_file_metadata('file.txt', metadata))