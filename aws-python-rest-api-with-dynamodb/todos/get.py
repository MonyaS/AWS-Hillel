import os

import boto3

from utils.serializer import deserialize_item

dynamodb = boto3.resource("dynamodb")


def get(event, context):
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # fetch todo from the database
    result = table.get_item(Key={"id": event["pathParameters"]["id"]})

    # create a response
    response = {
        "statusCode": 200,
        "body": deserialize_item(result["Item"]),
    }

    return response
