import os
import time
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
STACK_NAME = 'gestorPersonalTestApi'
TEMPLATE_FILE = 'api.yaml'
LAMBDA_BUCKET = os.getenv('S3_BUCKET')

# Initialize boto3 CloudFormation client
cf_client = boto3.client(
    'cloudformation',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_template_to_s3():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    s3_bucket = os.getenv('S3_BUCKET')
    s3_key = f'cloudformation/{TEMPLATE_FILE}'
    s3_client.upload_file(TEMPLATE_FILE, s3_bucket, s3_key)
    return f'https://{s3_bucket}.s3.{AWS_REGION}.amazonaws.com/{s3_key}'

def update_stack(template_url):
    try:
        response = cf_client.update_stack(
            StackName=STACK_NAME,
            TemplateURL=template_url,
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
            Parameters=[
                {
                    'ParameterKey': 'LambdaBucket',
                    'ParameterValue': LAMBDA_BUCKET
                }
            ]
        )
        print(f'Stack update initiated: {response["StackId"]}')
        wait_for_stack_completion()
    except cf_client.exceptions.ClientError as e:
        if 'No updates are to be performed' in str(e):
            print('No updates to be performed.')
        else:
            print(f'Update failed: {e}')
            delete_stack()
            wait_for_stack_deletion()
            create_stack(template_url)

def delete_stack():
    try:
        cf_client.delete_stack(StackName=STACK_NAME)
        print(f'Stack deletion initiated: {STACK_NAME}')
    except cf_client.exceptions.ClientError as e:
        print(f'Deletion failed: {e}')

def wait_for_stack_deletion():
    time_sleep = 5
    while True:
        print(f'Waiting {time_sleep} seconds')
        time.sleep(time_sleep)
        time_sleep += 5
        try:
            response = cf_client.describe_stacks(StackName=STACK_NAME)
            stack_status = response['Stacks'][0]['StackStatus']
            if stack_status == 'DELETE_COMPLETE':
                print(f'Stack {STACK_NAME} deleted successfully.')
                break
            else:
                print(f'Waiting for stack {STACK_NAME} to be deleted. Current status: {stack_status}')
        except cf_client.exceptions.ClientError as e:
            if 'does not exist' in str(e):
                print(f'Stack {STACK_NAME} does not exist.')
                break
            else:
                print(f'Error checking stack status: {e}')

def create_stack(template_url):
    try:
        response = cf_client.create_stack(
            StackName=STACK_NAME,
            TemplateURL=template_url,
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
            Parameters=[
                {
                    'ParameterKey': 'LambdaBucket',
                    'ParameterValue': LAMBDA_BUCKET
                }
            ]
        )
        print(f'Stack creation initiated: {response["StackId"]}')
        wait_for_stack_completion()
    except cf_client.exceptions.ClientError as e:
        print(f'Creation failed: {e}')

def wait_for_stack_completion():
    time_sleep = 5
    while True:
        print(f'Waiting {time_sleep} seconds')
        time.sleep(time_sleep)
        time_sleep += 5
        try:
            response = cf_client.describe_stacks(StackName=STACK_NAME)
            stack_status = response['Stacks'][0]['StackStatus']
            if stack_status in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']:
                print(f'Stack {STACK_NAME} completed successfully with status: {stack_status}')
                break
            elif stack_status in ['CREATE_FAILED', 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE']:
                print(f'Stack {STACK_NAME} failed with status: {stack_status}')
                break
            else:
                print(f'Waiting for stack {STACK_NAME} to complete. Current status: {stack_status}')
        except cf_client.exceptions.ClientError as e:
            print(f'Error checking stack status: {e}')

def main():
    template_url = upload_template_to_s3()
    update_stack(template_url)

if __name__ == '__main__':
    main()