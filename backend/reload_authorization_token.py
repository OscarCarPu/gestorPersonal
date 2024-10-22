import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('USER_PASSWORD')
ENV_FILE_PATH = '.env'

def get_authorization_token():
    client = boto3.client('cognito-idp', region_name='eu-south-2')
    
    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': USERNAME,
                'PASSWORD': PASSWORD
            },
            ClientId=CLIENT_ID
        )
        return response['AuthenticationResult']['IdToken']
    except client.exceptions.NotAuthorizedException:
        print("The username or password is incorrect.")
    except client.exceptions.UserNotFoundException:
        print("The user does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def set_key(file_path, key, value):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if line.startswith(key):
                file.write(f"{key}={value}\n")
            else:
                file.write(line)

def update_env_file(key, value, env_file_path=ENV_FILE_PATH):
    set_key(env_file_path, key, value)
    print(f"Updated {key} in {env_file_path} to {value}")

if __name__ == '__main__':
    token = get_authorization_token()
    if token:
        update_env_file('API_TOKEN', token)
        print(f"Authorization Token: {token}")