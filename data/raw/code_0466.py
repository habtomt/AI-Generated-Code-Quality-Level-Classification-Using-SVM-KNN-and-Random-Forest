"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
import os
import logging
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a class for scalable storage architecture
class ScalableStorage:
    def __init__(self):
        # Initialize AWS S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id='YOUR_API_KEY',
            aws_secret_access_key='YOUR_API_SECRET',
            region_name='YOUR_REGION'
        )

    # Method to upload files to S3
    def upload_file(self, bucket_name, object_name, file_path):
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f'File {file_path} does not exist')

            # Upload file to S3
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            logger.info(f'File {object_name} uploaded to {bucket_name} successfully')
        except FileNotFoundError as e:
            logger.error(e)
            raise
        except NoCredentialsError:
            logger.error('Credentials not found. Please check your AWS credentials.')
            raise
        except Exception as e:
            logger.error(f'Error uploading file: {e}')
            raise

    # Method to download files from S3
    def download_file(self, bucket_name, object_name, file_path):
        try:
            # Check if bucket and object exist
            if not self.s3_client.head_bucket(Bucket=bucket_name):
                raise Exception(f'Bucket {bucket_name} does not exist')
            if not self.s3_client.head_object(Bucket=bucket_name, Key=object_name):
                raise Exception(f'Object {object_name} does not exist in bucket {bucket_name}')

            # Download file from S3
            self.s3_client.download_file(bucket_name, object_name, file_path)
            logger.info(f'File {object_name} downloaded from {bucket_name} successfully')
        except Exception as e:
            logger.error(f'Error downloading file: {e}')
            raise

    # Method to list files in an S3 bucket
    def list_files(self, bucket_name):
        try:
            # List files in S3 bucket
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            files = [obj['Key'] for obj in response['Contents']]
            logger.info(f'Files in bucket {bucket_name}: {files}')
            return files
        except Exception as e:
            logger.error(f'Error listing files in bucket {bucket_name}: {e}')
            raise

# Example usage
if __name__ == '__main__':
    # Create a scalable storage instance
    storage = ScalableStorage()

    # Upload a file to S3
    bucket_name = 'my-bucket'
    object_name = 'example.txt'
    file_path = '/path/to/example.txt'
    storage.upload_file(bucket_name, object_name, file_path)

    # Download a file from S3
    download_file_path = '/path/to/download/example.txt'
    storage.download_file(bucket_name, object_name, download_file_path)

    # List files in an S3 bucket
    bucket_name = 'my-bucket'
    files = storage.list_files(bucket_name)
    print(files)