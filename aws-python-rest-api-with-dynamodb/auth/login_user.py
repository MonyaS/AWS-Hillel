import json
import os

import boto3

from utils.jwt_util import create_jwt_token

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ["USER_TABLE"])


def login_user(event, context):
    body = json.loads(event['body'])
    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Username and password are required'})
        }

    # Fetch the user from DynamoDB
    response = users_table.get_item(Key={'username': username})
    if 'Item' not in response:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Invalid username or password'})
        }

    user = response['Item']

    # Verify the password using bcrypt
    if password == user['password']:
        token = create_jwt_token(username)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Login successful',
                'token': token
            })
        }
    else:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Invalid username or password'})
        }
