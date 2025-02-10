import os

import boto3

from utils.auth_decorator import token_required
from utils.serializer import deserialize_item

dynamodb = boto3.resource("dynamodb")


@token_required
def get(event, context, username):
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # fetch todo from the database
    result = table.get_item(Key={"id": event["pathParameters"]["id"]})

    # create a response
    response = {
        "statusCode": 200,
        "body": deserialize_item(result["Item"]),
    }

    return response
