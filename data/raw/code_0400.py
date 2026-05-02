"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_003.txt
Run      : 1
"""

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def upload_to_glacier(bucket_name, file_name, object_name=None):
    """
    Upload a file to an S3 bucket using Glacier storage class

    :param bucket_name: Bucket to upload to
    :param file_name: File to upload
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Initialize a session using Amazon S3
    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(
            file_name, bucket_name, object_name,
            ExtraArgs={'StorageClass': 'GLACIER'}
        )
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials passed.")
        return False

    return True

if __name__ == "__main__":
    bucket = 'your-glacier-bucket-name'
    filename = 'your-file-path'

    success = upload_to_glacier(bucket, filename)
    if success:
        print(f"File {filename} successfully uploaded to Glacier storage class in bucket {bucket}.")
    else:
        print(f"Failed to upload {filename}.")