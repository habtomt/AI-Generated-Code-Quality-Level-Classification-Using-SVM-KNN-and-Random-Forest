"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_004.txt
Run      : 1
"""

import os
import boto3
from botocore.exceptions import NoCredentialsError
import redis
from pymongo import MongoClient
import time
from prometheus_client import start_http_server, Counter

# Define a counter for monitoring latency
REQUESTS = Counter('requests_total', 'Total number of requests')

# Set up AWS credentials (replace with your actual credentials)
AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'

# Set up Redis connection (replace with your actual Redis credentials)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'YOUR_REDIS_PASSWORD'

# Set up MongoDB connection (replace with your actual MongoDB credentials)
MONGO_URI = 'mongodb://localhost:27017/'

def upload_to_s3(local_file, bucket, s3_file):
    """
    Upload a file to an S3 bucket.
    """
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY)
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful: {s3_file} uploaded to {bucket}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def store_in_redis(key, value):
    """
    Store a value in Redis.
    """
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        r.set(key, value)
        print(f"Stored {value} in Redis with key {key}")
        return True
    except redis.exceptions.RedisError as e:
        print(f"Error storing in Redis: {e}")
        return False

def store_in_mongo(data):
    """
    Store data in MongoDB.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client['mydatabase']
        collection = db['mycollection']
        collection.insert_one(data)
        print("Data stored in MongoDB")
        return True
    except Exception as e:
        print(f"Error storing in MongoDB: {e}")
        return False

def monitor_latency():
    """
    Monitor latency using Prometheus.
    """
    start_http_server(8000)
    while True:
        time.sleep(1)

def main():
    # Upload a file to S3
    local_file = 'example.txt'
    bucket = 'my-bucket'
    s3_file = 'example.txt'
    upload_to_s3(local_file, bucket, s3_file)

    # Store a value in Redis
    key = 'my-key'
    value = 'my-value'
    store_in_redis(key, value)

    # Store data in MongoDB
    data = {'name': 'John', 'age': 30}
    store_in_mongo(data)

    # Monitor latency
    monitor_latency()

if __name__ == '__main__':
    main()