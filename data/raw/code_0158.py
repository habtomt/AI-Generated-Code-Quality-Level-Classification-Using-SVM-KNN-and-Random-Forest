import boto3
import time

DB_IDENTIFIER = 'your-db-instance-identifier'
CPU_THRESHOLD_HIGH = 75
CPU_THRESHOLD_LOW = 20
CHECK_INTERVAL = 300
REGION = 'us-east-1'

rds = boto3.client('rds', region_name=REGION)
cw = boto3.client('cloudwatch', region_name=REGION)

def get_cpu_utilization():
    metrics = cw.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': DB_IDENTIFIER}],
        StartTime=time.time() - 300,
        EndTime=time.time(),
        Period=60,
        Statistics=['Average']
    )
    return metrics['Datapoints'][0]['Average'] if metrics['Datapoints'] else 0

def scale_db(action):
    instance_class = 'db.m5.large' if action == 'scale_up' else 'db.t3.medium'
    print(f"Performing {action} to {instance_class}")
    try:
        rds.modify_db_instance(
            DBInstanceIdentifier=DB_IDENTIFIER,
            DBInstanceClass=instance_class,
            ApplyImmediately=True
        )
    except Exception as e:
        print(f"Scaling error: {e}")

if __name__ == "__main__":
    while True:
        cpu = get_cpu_utilization()
        print(f"CPU: {cpu}%")
        if cpu > CPU_THRESHOLD_HIGH:
            scale_db('scale_up')
        elif cpu < CPU_THRESHOLD_LOW:
            scale_db('scale_down')
        time.sleep(CHECK_INTERVAL)