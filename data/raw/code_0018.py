#!/usr/bin/env python3

import boto3
import json
import time

REGION = "us-east-1"

ec2 = boto3.client("ec2", region_name=REGION)
asg = boto3.client("autoscaling", region_name=REGION)
cloudwatch = boto3.client("cloudwatch", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)


DB_USER_DATA = """#!/bin/bash
apt-get update -y
apt-get install -y docker.io
systemctl start docker
systemctl enable docker

docker run -d --name postgres \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_DB=appdb \
  -p 5432:5432 postgres:15
"""


def create_launch_template():
    response = ec2.create_launch_template(
        LaunchTemplateName="db-vm-template",
        LaunchTemplateData={
            "ImageId": "ami-0c02fb55956c7d316",
            "InstanceType": "t3.micro",
            "UserData": DB_USER_DATA.encode("utf-8").decode("utf-8"),
            "SecurityGroupIds": [],
        },
    )
    return response["LaunchTemplate"]["LaunchTemplateId"]


def create_autoscaling_group(lt_id):
    asg.create_auto_scaling_group(
        AutoScalingGroupName="db-asg",
        LaunchTemplate={"LaunchTemplateId": lt_id},
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=1,
        VPCZoneIdentifier="subnet-xxxxxxxx",
    )


def create_sns_topic():
    topic = sns.create_topic(Name="db-alerts")
    return topic["TopicArn"]


def create_cpu_alarm(topic_arn):
    cloudwatch.put_metric_alarm(
        AlarmName="DBHighCPU",
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Statistic="Average",
        Period=300,
        EvaluationPeriods=2,
        Threshold=70.0,
        ComparisonOperator="GreaterThanThreshold",
        AlarmActions=[topic_arn],
        Dimensions=[
            {"Name": "AutoScalingGroupName", "Value": "db-asg"}
        ],
    )


def scale_out_policy():
    return asg.put_scaling_policy(
        AutoScalingGroupName="db-asg",
        PolicyName="scale-out",
        AdjustmentType="ChangeInCapacity",
        ScalingAdjustment=1,
    )


def scale_in_policy():
    return asg.put_scaling_policy(
        AutoScalingGroupName="db-asg",
        PolicyName="scale-in",
        AdjustmentType="ChangeInCapacity",
        ScalingAdjustment=-1,
    )


def main():
    print("Creating launch template...")
    lt_id = create_launch_template()

    print("Creating autoscaling group...")
    create_autoscaling_group(lt_id)

    print("Creating SNS topic...")
    topic_arn = create_sns_topic()

    print("Creating CloudWatch alarm...")
    create_cpu_alarm(topic_arn)

    print("Creating scaling policies...")
    scale_out_policy()
    scale_in_policy()

    print("Setup complete. Monitoring enabled.")

    while True:
        time.sleep(60)
        print("System running...")


if __name__ == "__main__":
    main()