"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_000.txt
Run      : 1
"""

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class S3Manager:
    def __init__(self, bucket_name, region_name='us-east-1', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID', aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY'):
        # Initialize the S3 client with the provided credentials and region
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
        self.bucket_name = bucket_name

    def upload_file(self, file_name, object_name=None, metadata=None):
        # Check if the object name is provided, if not use the file name
        if object_name is None:
            object_name = file_name
        try:
            # Prepare the extra arguments for the upload, including metadata if provided
            extra_args = {'Metadata': metadata} if metadata else {}
            # Upload the file to the specified S3 bucket
            self.s3.upload_file(file_name, self.bucket_name, object_name, ExtraArgs=extra_args)
            print(f"File {file_name} uploaded to {self.bucket_name}/{object_name}")
        except FileNotFoundError:
            # Handle the case where the file is not found
            print("The file was not found.")
        except NoCredentialsError:
            # Handle the case where AWS credentials are not available
            print("Credentials not available.")
        except ClientError as e:
            # Handle any other client errors
            print(f"Failed to upload file: {e}")

    def download_file(self, object_name, file_name):
        try:
            # Download the file from the specified S3 bucket
            self.s3.download_file(self.bucket_name, object_name, file_name)
            print(f"File {object_name} downloaded from {self.bucket_name} to {file_name}")
        except NoCredentialsError:
            # Handle the case where AWS credentials are not available
            print("Credentials not available.")
        except ClientError as e:
            # Handle any other client errors
            print(f"Failed to download file: {e}")

    def get_file_metadata(self, object_name):
        try:
            # Retrieve the metadata of the file from the specified S3 bucket
            response = self.s3.head_object(Bucket=self.bucket_name, Key=object_name)
            # Return the metadata if available, otherwise return an empty dictionary
            return response.get('Metadata', {})
        except ClientError as e:
            # Handle any client errors
            print(f"Failed to get metadata: {e}")
            return None

# Usage Example
if __name__ == "__main__":
    # Replace with your actual AWS credentials and bucket name
    s3_manager = S3Manager(bucket_name='YOUR_S3_BUCKET_NAME', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID', aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY')
    
    # Upload a file with metadata
    s3_manager.upload_file('path/to/your/file.txt', metadata={'author': 'John Doe', 'description': 'Sample file'})
    
    # Download a file
    s3_manager.download_file('file.txt', 'path/to/download/destination.txt')
    
    # Get file metadata
    metadata = s3_manager.get_file_metadata('file.txt')
    print(f"Metadata for file.txt: {metadata}")