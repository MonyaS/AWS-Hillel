import datetime
import json
import os
from functools import wraps

import boto3
import jwt

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users')


def token_required(func):
    @wraps(func)
    def check_jwt(event, context, *args, **kwargs):
        headers = event["headers"]
        if "Authorization" not in headers.keys():
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Token is missing'})
            }
        token = headers["Authorization"]
        try:
            # Strip 'Bearer ' prefix and decode token
            token = token.split(' ')

            if len(token) != 2:
                raise jwt.InvalidTokenError

            payload = jwt.decode(token[1], os.environ["SECRET_KEY"], algorithms=["HS256"])

            if payload["expiration"] < datetime.datetime.now():
                raise jwt.ExpiredSignatureError

            username = payload["sub"]

            result = users_table.get_item(Key={"username": username})

            if 'Item' not in result:
                raise jwt.InvalidTokenError

            return func(event, context, username, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Token has expired'})
            }
        except jwt.InvalidTokenError:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Invalid token'})
            }

    return check_jwt
