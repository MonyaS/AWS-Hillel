import json

import boto3

from utils.auth_decorator import token_required

dynamodb = boto3.resource("dynamodb")


@token_required
def test(event, context, username):
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(username),
    }

    return response
