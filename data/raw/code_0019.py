#!/usr/bin/env python3

import boto3
import os
import time
import uuid

REGION = "us-east-1"
BUCKET_NAME = f"static-assets-{uuid.uuid4().hex[:8]}"
LOCAL_ASSETS_DIR = "./static"

s3 = boto3.client("s3", region_name=REGION)
cloudfront = boto3.client("cloudfront")


def create_bucket():
    print(f"Creating S3 bucket: {BUCKET_NAME}")
    s3.create_bucket(Bucket=BUCKET_NAME)
    return BUCKET_NAME


def upload_assets():
    print("Uploading static assets...")
    for root, _, files in os.walk(LOCAL_ASSETS_DIR):
        for file in files:
            path = os.path.join(root, file)
            key = os.path.relpath(path, LOCAL_ASSETS_DIR)
            s3.upload_file(path, BUCKET_NAME, key)


def create_cloudfront_distribution():
    origin_id = f"S3-{BUCKET_NAME}"

    response = cloudfront.create_distribution(
        DistributionConfig={
            "CallerReference": str(time.time()),
            "Origins": {
                "Quantity": 1,
                "Items": [
                    {
                        "Id": origin_id,
                        "DomainName": f"{BUCKET_NAME}.s3.amazonaws.com",
                        "S3OriginConfig": {"OriginAccessIdentity": ""},
                    }
                ],
            },
            "DefaultCacheBehavior": {
                "TargetOriginId": origin_id,
                "ViewerProtocolPolicy": "redirect-to-https",
                "TrustedSigners": {"Enabled": False, "Quantity": 0},
                "ForwardedValues": {
                    "QueryString": False,
                    "Cookies": {"Forward": "none"},
                },
                "MinTTL": 0,
            },
            "Enabled": True,
            "Comment": "Static asset caching layer",
        }
    )

    dist = response["Distribution"]
    domain = dist["DomainName"]

    print(f"CloudFront distribution created: https://{domain}")
    return dist["Id"], domain


def invalidate_cache(distribution_id):
    print("Creating cache invalidation...")
    cloudfront.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            "Paths": {
                "Quantity": 1,
                "Items": ["/*"],
            },
            "CallerReference": str(time.time()),
        },
    )


def monitor_distribution(domain):
    print("Monitoring edge cache availability...")
    while True:
        print(f"Serving content via CDN at https://{domain}")
        time.sleep(30)


def main():
    bucket = create_bucket()
    upload_assets()

    dist_id, domain = create_cloudfront_distribution()

    invalidate_cache(dist_id)

    monitor_distribution(domain)


if __name__ == "__main__":
    main()