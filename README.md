# Lambda Instance Refresh Python Function

This repository contains a Lambda function written in Python that allows you to trigger an instance refresh for a specified Auto Scaling group in Amazon Web Services (AWS). An instance refresh involves replacing instances in the Auto Scaling group to ensure that they are running the latest version of the specified launch template or configuration.

## Prerequisites

- AWS Account: You should have an active AWS account to deploy and use this Lambda function.
- AWS CLI: Ensure that the AWS Command Line Interface (CLI) is installed and properly configured with your AWS credentials.

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/HarestWill/instance-refresh.git
cd instance-refresh
```

2. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

3. Open refresh.py and modify the following variables:

autoscaling_group_name: Specify the name of the Auto Scaling group that you want to refresh.
Deploy the Lambda function to AWS using the AWS CLI:

bash
Copy code
aws lambda create-function --function-name InstanceRefreshFunction \
    --runtime python3.8 --role your-lambda-role-arn \
    --handler lambda_function.lambda_handler --zip-file fileb://lambda_function.zip
Replace your-lambda-role-arn with the ARN of the IAM role that the Lambda function will assume.

Create an event source (such as an S3 bucket, an SNS topic, or an API Gateway) that triggers the Lambda function when needed.
Triggering the Function
Once the function is deployed and properly triggered, it will initiate an instance refresh for the specified Auto Scaling group. Monitor the progress of the instance refresh in the AWS Management Console.

4. Clean Up
Remember to remove the Lambda function and any associated resources when they are no longer needed to avoid incurring unnecessary costs.

