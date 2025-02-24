import os
import time

import boto3

from utils.auth_decorator import token_required
from utils.serializer import deserialize_item

dynamodb = boto3.resource("dynamodb")


@token_required
def mark_checked(event, context, username):
    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # update the todo in the database
    result = table.update_item(
        Key={"id": event["pathParameters"]["id"]},
        ExpressionAttributeNames={
            "#user": "user"
        },
        ExpressionAttributeValues={
            ":checked": True,
            ":updatedAt": timestamp,
            ":username_val": username
        },
        UpdateExpression="SET checked = :checked, "
                         "updatedAt = :updatedAt",
        ConditionExpression="#user = :username_val",
        ReturnValues="ALL_NEW",
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": deserialize_item(result["Attributes"]),
    }

    return response
