import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
asg = boto3.client('autoscaling', region_name='us-east-1')

def deploy_db_with_scaling():
    # 1. Create Launch Template
    ec2.create_launch_template(
        LaunchTemplateName='db-launch-template',
        LaunchTemplateData={
            'ImageId': 'ami-0abcdef1234567890',
            'InstanceType': 't3.medium',
            'UserData': 'IyEvYmluL2Jhc2gNCmFwdCB1cGRhdGUgJiYgYXB0IGluc3RhbGwgbXlzcWwtc2VydmVyIC15', # Base64 script to install DB
            'Monitoring': {'Enabled': True}
        }
    )

    # 2. Create Auto Scaling Group
    asg.create_auto_scaling_group(
        AutoScalingGroupName='db-asg',
        LaunchTemplate={'LaunchTemplateName': 'db-launch-template', 'Version': '$Latest'},
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=1,
        VPCZoneIdentifier='subnet-12345abc'
    )

    # 3. Define Scaling Policy based on CPU
    asg.put_scaling_policy(
        AutoScalingGroupName='db-asg',
        PolicyName='cpu-scaling-policy',
        PolicyType='TargetTrackingScaling',
        TargetTrackingConfiguration={
            'PredefinedMetricSpecification': {'PredefinedMetricType': 'ASGAverageCPUUtilization'},
            'TargetValue': 70.0
        }
    )

if __name__ == "__main__":
    deploy_db_with_scaling()