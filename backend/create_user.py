import os
import boto3
from dotenv import load_dotenv, set_key

# Load environment variables from .env file
load_dotenv()

USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
NEW_USERNAME = os.getenv('USERNAME')
NEW_PASSWORD = os.getenv('USER_PASSWORD')
ENV_FILE_PATH = '.env'

def create_or_update_user():
    client = boto3.client('cognito-idp', region_name='eu-south-2')
    
    try:
        # Create a new user
        response = client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=NEW_USERNAME,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': 'user@example.com'
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ],
            TemporaryPassword=NEW_PASSWORD,
            MessageAction='SUPPRESS'
        )
        print(f"User {NEW_USERNAME} created successfully.")
        
        # Set the user's password
        client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=NEW_USERNAME,
            Password=NEW_PASSWORD,
            Permanent=True
        )
        print(f"Password for user {NEW_USERNAME} set successfully.")
        
    except client.exceptions.UsernameExistsException:
        print("The username already exists. Updating the user.")
        # Update the user's attributes
        client.admin_update_user_attributes(
            UserPoolId=USER_POOL_ID,
            Username=NEW_USERNAME,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': 'user@example.com'
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ]
        )
        # Set the user's password
        client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=NEW_USERNAME,
            Password=NEW_PASSWORD,
            Permanent=True
        )
        print(f"Password for user {NEW_USERNAME} updated successfully.")
    except client.exceptions.PasswordResetRequiredException:
        print("Password reset required for the user. Resetting password.")
        reset_password()
    except Exception as e:
        print(f"An error occurred: {e}")

def reset_password():
    client = boto3.client('cognito-idp', region_name='eu-south-2')
    
    try:
        # Initiate the password reset
        response = client.admin_reset_user_password(
            UserPoolId=USER_POOL_ID,
            Username=NEW_USERNAME
        )
        print(f"Password reset initiated for user {NEW_USERNAME}.")
        
        # Confirm the password reset with a new password
        client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=NEW_USERNAME,
            Password=NEW_PASSWORD,
            Permanent=True
        )
        print(f"Password for user {NEW_USERNAME} reset successfully.")
    except client.exceptions.UserNotFoundException:
        print("The user does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_or_update_user_pool_client():
    client = boto3.client('cognito-idp', region_name='eu-south-2')
    
    try:
        # Create a user pool client with USER_PASSWORD_AUTH and ALLOW_REFRESH_TOKEN_AUTH flow enabled
        response = client.create_user_pool_client(
            UserPoolId=USER_POOL_ID,
            ClientName='MyAppClient',
            GenerateSecret=False,
            ExplicitAuthFlows=['ALLOW_USER_PASSWORD_AUTH', 'ALLOW_REFRESH_TOKEN_AUTH']
        )
        client_id = response['UserPoolClient']['ClientId']
        print(f"User pool client created successfully. Client ID: {client_id}")
        return client_id
    except client.exceptions.InvalidParameterException as e:
        if 'client already exists' in str(e):
            print("The client already exists. Updating the client.")
            response = client.update_user_pool_client(
                UserPoolId=USER_POOL_ID,
                ClientId=CLIENT_ID,
                ExplicitAuthFlows=['ALLOW_USER_PASSWORD_AUTH', 'ALLOW_REFRESH_TOKEN_AUTH']
            )
            client_id = response['UserPoolClient']['ClientId']
            print(f"User pool client updated successfully. Client ID: {client_id}")
            return client_id
        else:
            print(f"An error occurred: {e}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_env_file(key, value, env_file_path=ENV_FILE_PATH):
    set_key(env_file_path, key, value)
    print(f"Updated {key} in {env_file_path} to {value}")

if __name__ == '__main__':
    create_or_update_user()
    client_id = create_or_update_user_pool_client()
    if client_id:
        update_env_file('CLIENT_ID', client_id)
        print(f"Environment variable CLIENT_ID set to: {client_id}")