import os
import zipfile
import boto3
from dotenv import load_dotenv

# Load environment variables from .env fºile
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY_PREFIX = 'gestorpersonal/backend/lambdas/'

# Initialize boto3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def compress_lambda_files():
    lambda_folder = 'lambdas'
    for root, dirs, files in os.walk(lambda_folder):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                zip_file_path = file_path.replace('.py', '.zip')
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    zipf.write(file_path, os.path.basename(file_path))
                yield zip_file_path

def upload_to_s3(zip_file_path):
    s3_key = os.path.join(S3_KEY_PREFIX, os.path.basename(zip_file_path))
    s3_client.upload_file(zip_file_path, S3_BUCKET, s3_key)
    print(f'Uploaded {zip_file_path} to s3://{S3_BUCKET}/{s3_key}')

def main():
    for zip_file_path in compress_lambda_files():
        upload_to_s3(zip_file_path)

if __name__ == '__main__':
    main()