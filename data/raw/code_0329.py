"""
Auto-generated Python code
Scenario : Cloud Database Services
Prompt   : response_002.txt
Run      : 2
"""

import os
import boto3
from botocore.exceptions import ClientError

# Set AWS region
AWS_REGION = 'YOUR_AWS_REGION'

# Set AWS credentials
AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY'

# Set database credentials
DB_USERNAME = 'YOUR_DB_USERNAME'
DB_PASSWORD = 'YOUR_DB_PASSWORD'

# Set database name
DB_NAME = 'YOUR_DB_NAME'

# Set encryption key
ENCRYPTION_KEY = 'YOUR_ENCRYPTION_KEY'

def create_iam_role():
    """
    Create an IAM role for database access
    """
    iam = boto3.client('iam', aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION)
    
    try:
        # Create IAM role
        response = iam.create_role(
            RoleName='cloud-database-role',
            AssumeRolePolicyDocument={
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {'Service': 'rds.amazonaws.com'},
                        'Action': 'sts:AssumeRole'
                    }
                ]
            }
        )
        
        print(f"IAM role created: {response['Role']['RoleName']}")
        
    except ClientError as e:
        print(f"Error creating IAM role: {e.response['Error']['Message']}")


def attach_policy_to_iam_role():
    """
    Attach a policy to the IAM role for database access
    """
    iam = boto3.client('iam', aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION)
    
    try:
        # Create IAM policy
        policy = iam.create_policy(
            PolicyName='cloud-database-policy',
            PolicyDocument={
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Action': 'rds:*',
                        'Resource': '*'
                    }
                ]
            }
        )
        
        # Attach policy to IAM role
        iam.attach_role_policy(
            RoleName='cloud-database-role',
            PolicyArn=policy['Policy']['Arn']
        )
        
        print("Policy attached to IAM role")
        
    except ClientError as e:
        print(f"Error attaching policy to IAM role: {e.response['Error']['Message']}")


def create_database():
    """
    Create a cloud database
    """
    rds = boto3.client('rds', aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION)
    
    try:
        # Create database
        response = rds.create_db_instance(
            DBInstanceIdentifier=DB_NAME,
            Engine='postgres',
            MasterUsername=DB_USERNAME,
            MasterUserPassword=DB_PASSWORD,
            DBInstanceClass='db.t2.micro',
            VpcSecurityGroupIds=['YOUR_VPC_SECURITY_GROUP_ID'],
            AllocatedStorage=20,
            MultiAZ=True,
            DBInstanceRoleArn='arn:aws:iam::YOUR_ACCOUNT_ID:role/cloud-database-role',
            KmsKeyId=ENCRYPTION_KEY
        )
        
        print(f"Database created: {response['DBInstance']['DBInstanceIdentifier']}")
        
    except ClientError as e:
        print(f"Error creating database: {e.response['Error']['Message']}")


def enable_encryption():
    """
    Enable encryption for the database
    """
    rds = boto3.client('rds', aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION)
    
    try:
        # Create encryption key
        response = rds.create_db_instance(
            DBInstanceIdentifier=DB_NAME,
            Engine='postgres',
            MasterUsername=DB_USERNAME,
            MasterUserPassword=DB_PASSWORD,
            DBInstanceClass='db.t2.micro',
            VpcSecurityGroupIds=['YOUR_VPC_SECURITY_GROUP_ID'],
            AllocatedStorage=20,
            MultiAZ=True,
            DBInstanceRoleArn='arn:aws:iam::YOUR_ACCOUNT_ID:role/cloud-database-role',
            KmsKeyId=ENCRYPTION_KEY
        )
        
        # Enable encryption for the database
        rds.modify_db_instance(
            DBInstanceIdentifier=DB_NAME,
            EnableCloudwatchLogsExports=['GENERAL_LOG']
        )
        
        print("Encryption enabled for the database")
        
    except ClientError as e:
        print(f"Error enabling encryption: {e.response['Error']['Message']}")


def enable_audit_logging():
    """
    Enable audit logging for the database
    """
    rds = boto3.client('rds', aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION)
    
    try:
        # Enable audit logging for the database
        rds.enable_cloudwatch_logs_exports(
            DBInstanceIdentifier=DB_NAME,
            LogTypes=['GENERAL_LOG']
        )
        
        print("Audit logging enabled for the database")
        
    except ClientError as e:
        print(f"Error enabling audit logging: {e.response['Error']['Message']}")


def main():
    # Create IAM role
    create_iam_role()
    
    # Attach policy to IAM role
    attach_policy_to_iam_role()
    
    # Create database
    create_database()
    
    # Enable encryption
    enable_encryption()
    
    # Enable audit logging
    enable_audit_logging()


if __name__ == "__main__":
    main()