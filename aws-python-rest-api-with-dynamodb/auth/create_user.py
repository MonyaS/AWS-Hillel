import json
import os
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ["USER_TABLE"])


def create_user(event, context):
    if not event.get('body'):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No body in request'})
        }

    body = json.loads(event['body'])
    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Username and password are required'})
        }

    # Check
    result = users_table.get_item(Key={"username": username})
    if 'Item' in result:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Username already exists.'})
        }

    # Store the user in DynamoDB
    users_table.put_item(
        Item={"id": str(uuid.uuid1()), 'username': username, 'password': password}
    )
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'User registered successfully'})
    }
