import boto3
from time import sleep
import os

def lambda_handler(event, context):
    print('handled event:', event)
    asg_client = boto3.client('autoscaling')
    asg_name = ""
    min_instances = int(os.environ['MIN_INSTANCES'])
    max_instances = int(os.environ['MAX_INSTANCES'])
    MinHealthyPercentage = int(os.environ['MIN_HEALTHY_PERCENT'])
    MaxHealthyPercentage = int(os.environ['MAX_HEALTHY_PERCENT'])
    asg = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])

    max_capacity = asg['AutoScalingGroups'][0]['MaxSize']

    # Describe the Auto Scaling Group
    asg = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    current_capacity = asg['AutoScalingGroups'][0]['DesiredCapacity']

    # Get the current number of instances in the ASG
    instance_count = asg['AutoScalingGroups'][0]['DesiredCapacity']
    
    # Remove the scaling protection for old instances
    instance_ids = asg['AutoScalingGroups'][0]['Instances']
    for instance in instance_ids:
        asg_client.set_instance_protection(InstanceIds=[instance['InstanceId']], AutoScalingGroupName=asg_name, ProtectedFromScaleIn=False)

    if instance_count >= max_instances:
        # Start the instance refresh 
        asg_client.start_instance_refresh(AutoScalingGroupName=asg_name, 
                               Strategy='Rolling', 
                               Preferences={'MinHealthyPercentage': MinHealthyPercentage})

        print(f'Instance refresh started for ASG {asg_name}')
        
    elif instance_count > min_instances and instance_count < max_instances:
       # Start the instance refresh 
        asg_client.start_instance_refresh(AutoScalingGroupName=asg_name, 
                               Strategy='Rolling', 
                               Preferences={'MinHealthyPercentage': MaxHealthyPercentage})

        print(f'Instance refresh started for ASG {asg_name}')
        
    elif instance_count == min_instances:
        # Start an additional instance first
        asg_client.set_desired_capacity(AutoScalingGroupName=asg_name, DesiredCapacity=current_capacity + 1)
        
        # Wait for instances to be in running state
        waiter = asg_client.get_waiter('instance_in_service')
        waiter.wait(AutoScalingGroupName=asg_name)
        
        # Start the instance refresh 
        asg_client.start_instance_refresh(AutoScalingGroupName=asg_name)
        print(f'An additional instance was started and then instance refresh started for ASG {asg_name}')
    
    
     # Add the scaling protection for new instances
    asg_client.update_auto_scaling_group(AutoScalingGroupName=asg_name, NewInstancesProtectedFromScaleIn=True)


    # Wait for the instance refresh to complete
    while True:
        response = asg_client.describe_instance_refreshes(AutoScalingGroupName=asg_name)
        if response['InstanceRefreshes'][0]['Status'] == 'Successful':
            break
        sleep(30)
    print(f"Instance refresh for group {asg_name} is a Success")
