import json
import os

import boto3

from utils.auth_decorator import token_required
from utils.serializer import deserialize_item

dynamodb = boto3.resource("dynamodb")


@token_required
def list_lambda(event, context, username):
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # fetch all todos from the database
    result = table.scan()

    items = []
    for item in result['Items']:
        items.append(deserialize_item(item))

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"items": items}),
    }

    return response
