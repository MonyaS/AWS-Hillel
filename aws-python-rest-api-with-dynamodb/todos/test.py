import json

import boto3

dynamodb = boto3.resource("dynamodb")


def test(event, context):
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(event),
    }

    return response
