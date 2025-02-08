import json

import bcrypt
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users')


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
    if 'Item' not in result:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Username already exists.'})
        }

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Store the user in DynamoDB
    users_table.put_item(
        Item={'username': username, 'password': hashed_password.decode('utf-8')}
    )
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'User registered successfully'})
    }
