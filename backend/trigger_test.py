import requests
import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

def empty_database():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GestorPersonal')
    
    # Use pagination to handle large datasets
    scan_kwargs = {}
    done = False
    start_key = None
    
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        with table.batch_writer() as batch:
            for item in response.get('Items', []):
                batch.delete_item(Key={'id': item['id'], 'entidad': item['entidad']})
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
    return True

def test_api_endpoint(type, endpoint, body, expected_response):
    base_url = os.getenv('API_URL')
    if base_url is None:
        raise ValueError("API_URL environment variable is not set")
    
    url = base_url + endpoint
    token = os.getenv('API_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    if type.upper() in ['GET', 'DELETE']:
        response = requests.request(type, url, headers=headers)
    else:
        response = requests.request(type, url, headers=headers, data=json.dumps(body))
    
    if response.status_code != expected_response['status']:
        raise Exception(f'Expected body {expected_response["status"]} but received {response.status_code}, body: {response.text}')
    
    actual_body = response.json()
    expected_body = expected_response['body']
    
    # Remove 'datetime_creacion' from both actual and expected bodies
    if 'datetime_creacion' in actual_body:
        del actual_body['datetime_creacion']
    if 'datetime_creacion' in expected_body:
        del expected_body['datetime_creacion']
    
    # Compare JSON objects to ensure order doesn't matter
    if json.dumps(actual_body, sort_keys=True) != json.dumps(expected_body, sort_keys=True):
        raise Exception(f'Expected body {expected_body} but received {actual_body}')
    
    return True

def read_json_files(file_paths):
    json_arrays = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            json_arrays.append((file_path, json.load(file)))
    return json_arrays

def run_tests(json_arrays):
    total_tests = 0
    success_count = 0
    for file_path, json_array in json_arrays:
        for test_case in json_array:
            total_tests += 1
            try:
                if test_api_endpoint(test_case['type'], test_case['endpoint'], test_case['body'], test_case['expected_response']):
                    success_count += 1
            except Exception as e:
                print(f'Error in test case: {test_case["test_id"]} from file: {file_path}')
                print(e)
    print(f'Successful tests: {success_count}/{total_tests}')
    return success_count

file_paths = []
for root, dirs, files in os.walk('tests'):
    for file in files:
        if file.endswith('.json'):
            file_paths.append(os.path.join(root, file))

empty_database()
json_arrays = read_json_files(file_paths)
run_tests(json_arrays)