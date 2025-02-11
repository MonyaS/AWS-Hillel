import os

import boto3
from boto3.dynamodb.conditions import Key

from utils.auth_decorator import token_required
from utils.serializer import deserialize_item

dynamodb = boto3.resource("dynamodb")


@token_required
def get(event, context, username):
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # fetch todo from the database
    result = table.scan(
        FilterExpression=Key('id').eq(event["pathParameters"]["id"]) & Key('user').eq(username)
    )
    if "Items" in result.keys():
        # create a response
        response = {
            "statusCode": 200,
            "body": deserialize_item(result["Items"][0]),
        }
    else:
        return {
            "statusCode": 404,
            "message": "Not found",
        }

    return response
