"""
Auto-generated Python code
Scenario : Cloud Database Services
Prompt   : response_002.txt
Run      : 3
"""

# Import required libraries
import os
import yaml
from google.cloud import storage
from google.cloud import secretmanager
from google.cloud import bigquery
from google.cloud import logging

# Load configuration from YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['credentials']
os.environ['PROJECT_ID'] = config['project_id']

# Authenticate with Google Cloud
try:
    from google.oauth2 import service_account
    credential = service_account.Credentials.from_service_account_file(
        config['credentials'],
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
except Exception as e:
    print(f"Error authenticating with Google Cloud: {e}")
    exit(1)

# Create Storage Bucket with encryption at rest
try:
    storage_client = storage.Client(credentials=credential)
    bucket_name = config['storage_bucket_name']
    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = 'REGIONAL'
    bucket.encryption = storage.BucketEncryption(
        default_kms_key_name=config['kms_key_name']
    )
    bucket.update()
    print(f"Created Storage Bucket {bucket_name} with encryption at rest")
except Exception as e:
    print(f"Error creating Storage Bucket: {e}")

# Create BigQuery Dataset with encryption at rest
try:
    bigquery_client = bigquery.Client(credentials=credential)
    dataset_name = config['bigquery_dataset_name']
    dataset = bigquery_client.dataset(dataset_name)
    dataset.location = config['bigquery_location']
    dataset.default_table_encryption = bigquery.TableEncryption(
        kms_key_name=config['kms_key_name']
    )
    dataset.update()
    print(f"Created BigQuery Dataset {dataset_name} with encryption at rest")
except Exception as e:
    print(f"Error creating BigQuery Dataset: {e}")

# Set up role-based access control
try:
    iam_client = bigquery_client.service_account()
    iam_client.create_role(
        dataset_name,
        'read_only',
        roles=['roles/bigquery.dataReader']
    )
    iam_client.create_role(
        dataset_name,
        'read_write',
        roles=['roles/bigquery.dataEditor']
    )
    print("Set up role-based access control")
except Exception as e:
    print(f"Error setting up role-based access control: {e}")

# Set up audit logging
try:
    logging_client = logging.Client(credentials=credential)
    logging_bucket_name = config['logging_bucket_name']
    logging_bucket = storage_client.bucket(logging_bucket_name)
    logging_client.create_sink(
        dataset_name,
        logging_bucket.name,
        logging.BucketDestination(
            bucket=logging_bucket.name,
            prefix=config['logging_prefix']
        )
    )
    print("Set up audit logging")
except Exception as e:
    print(f"Error setting up audit logging: {e}")