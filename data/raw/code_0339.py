"""
Auto-generated Python code
Scenario : Cloud Hosting
Prompt   : response_002.txt
Run      : 1
"""

import boto3
import os

# AWS credentials
AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'
AWS_REGION = 'YOUR_AWS_REGION'

# Database settings
DB_ENGINE = 'mysql'  # or 'postgres', 'oracle', etc.
DB_INSTANCE_CLASS = 'db.t2.micro'
DB_STORAGE = 20  # GB
DB_USERNAME = 'YOUR_DB_USERNAME'
DB_PASSWORD = 'YOUR_DB_PASSWORD'
DB_NAME = 'YOUR_DB_NAME'

# Security group settings
SECURITY_GROUP_NAME = 'YOUR_SECURITY_GROUP_NAME'
SECURITY_GROUP_DESCRIPTION = 'YOUR_SECURITY_GROUP_DESCRIPTION'

# Auto scaling settings
AUTO_SCALING_GROUP_NAME = 'YOUR_AUTO_SCALING_GROUP_NAME'
AUTO_SCALING_POLICY_NAME = 'YOUR_AUTO_SCALING_POLICY_NAME'

# CloudWatch settings
CLOUDWATCH_ALARM_NAME = 'YOUR_CLOUDWATCH_ALARM_NAME'
CLOUDWATCH_ALARM_DESCRIPTION = 'YOUR_CLOUDWATCH_ALARM_DESCRIPTION'
CLOUDWATCH_ALARM_THRESHOLD = 80  # percentage

def create_database():
    # Create an RDS client
    rds = boto3.client('rds', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

    # Create a database instance
    try:
        response = rds.create_db_instance(
            DBInstanceIdentifier=DB_NAME,
            DBInstanceClass=DB_INSTANCE_CLASS,
            Engine=DB_ENGINE,
            MasterUsername=DB_USERNAME,
            MasterUserPassword=DB_PASSWORD,
            AllocatedStorage=DB_STORAGE
        )
        print('Database instance created:', response['DBInstance']['DBInstanceIdentifier'])
    except Exception as e:
        print('Error creating database instance:', str(e))

def create_security_group():
    # Create an EC2 client
    ec2 = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

    # Create a security group
    try:
        response = ec2.create_security_group(
            GroupName=SECURITY_GROUP_NAME,
            Description=SECURITY_GROUP_DESCRIPTION
        )
        print('Security group created:', response['GroupId'])
    except Exception as e:
        print('Error creating security group:', str(e))

def create_auto_scaling_group():
    # Create an Auto Scaling client
    asg = boto3.client('autoscaling', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

    # Create an Auto Scaling group
    try:
        response = asg.create_auto_scaling_group(
            AutoScalingGroupName=AUTO_SCALING_GROUP_NAME,
            LaunchConfigurationName='YOUR_LAUNCH_CONFIGURATION_NAME',
            MinSize=1,
            MaxSize=10
        )
        print('Auto Scaling group created:', response['AutoScalingGroupName'])
    except Exception as e:
        print('Error creating Auto Scaling group:', str(e))

def create_cloudwatch_alarm():
    # Create a CloudWatch client
    cw = boto3.client('cloudwatch', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

    # Create a CloudWatch alarm
    try:
        response = cw.put_metric_alarm(
            AlarmName=CLOUDWATCH_ALARM_NAME,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='CPUUtilization',
            Namespace='AWS/RDS',
            Period=300,
            Statistic='Average',
            Threshold=CLOUDWATCH_ALARM_THRESHOLD,
            ActionsEnabled=True,
            AlarmDescription=CLOUDWATCH_ALARM_DESCRIPTION,
            AlarmActions=['arn:aws:sns:' + AWS_REGION + ':' + AWS_ACCESS_KEY + ':YOUR_SNS_TOPIC']
        )
        print('CloudWatch alarm created:', response['AlarmArn'])
    except Exception as e:
        print('Error creating CloudWatch alarm:', str(e))

if __name__ == '__main__':
    create_database()
    create_security_group()
    create_auto_scaling_group()
    create_cloudwatch_alarm()