import json
import os

import jwt_util


def lambda_handler(event, context):
    token = event['authorizationToken']  # Bearer token
    try:
        # Strip 'Bearer ' prefix and decode token
        token = token.split(' ')[1]
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])

        # If token is valid, return policy allowing access
        return {
            'principalId': payload['sub'],
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [{
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow',
                    'Resource': event['methodArn']
                }]
            }
        }
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
