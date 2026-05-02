"""
Auto-generated Python code
Scenario : Cloud Database Services
Prompt   : response_001.txt
Run      : 1
"""

import boto3
import time

# Configuration variables
DB_IDENTIFIER = 'your-db-instance-identifier'
CPU_THRESHOLD_HIGH = 75  # CPU percent to scale up at
CPU_THRESHOLD_LOW = 20   # CPU percent to scale down at
CHECK_INTERVAL = 300     # Check every 5 minutes (300 seconds)
REGION = 'your-region'   # e.g., 'us-east-1'
SCALE_UP_INSTANCE_TYPE = 'db.m5.large'  # Example: change to a larger instance type
SCALE_DOWN_INSTANCE_TYPE = 'db.t3.medium'  # Example: change to a smaller instance type

def get_rds_client():
    # Create an RDS client
    return boto3.client('rds', region_name=REGION)

def get_cloudwatch_client():
    # Create a CloudWatch client
    return boto3.client('cloudwatch', region_name=REGION)

def get_current_cpu_utilization(cloudwatch, db_identifier):
    # Get the current CPU utilization of the database instance
    try:
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': db_identifier}],
            StartTime=time.time() - 300,  # Look at the past 5 minutes
            EndTime=time.time(),
            Period=60,
            Statistics=['Average']
        )

        if len(metrics['Datapoints']) == 0:
            return 0
        return metrics['Datapoints'][0]['Average']
    except Exception as e:
        print(f"Error getting CPU utilization: {e}")
        return 0

def scale_db_instances(rds_client, db_identifier, action):
    # Scale the database instances up or down
    if action == 'scale_up':
        print("Scaling up the instances.")
        try:
            rds_client.modify_db_instance(
                DBInstanceIdentifier=db_identifier,
                DBInstanceClass=SCALE_UP_INSTANCE_TYPE,
                ApplyImmediately=True
            )
        except Exception as e:
            print(f"Error scaling up: {e}")
    elif action == 'scale_down':
        print("Scaling down the instances.")
        try:
            rds_client.modify_db_instance(
                DBInstanceIdentifier=db_identifier,
                DBInstanceClass=SCALE_DOWN_INSTANCE_TYPE,
                ApplyImmediately=True
            )
        except Exception as e:
            print(f"Error scaling down: {e}")

def main():
    rds_client = get_rds_client()
    cloudwatch_client = get_cloudwatch_client()

    while True:
        cpu_utilization = get_current_cpu_utilization(cloudwatch_client, DB_IDENTIFIER)
        print(f"Current CPU Utilization: {cpu_utilization}%")

        if cpu_utilization > CPU_THRESHOLD_HIGH:
            scale_db_instances(rds_client, DB_IDENTIFIER, 'scale_up')
        elif cpu_utilization < CPU_THRESHOLD_LOW:
            scale_db_instances(rds_client, DB_IDENTIFIER, 'scale_down')

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()