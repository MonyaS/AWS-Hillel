import json
import logging
import os
import time

import boto3

from utils.auth_decorator import token_required
from utils.serializer import deserialize_item

dynamodb = boto3.resource("dynamodb")


@token_required
def update(event, context, username):
    data = json.loads(event["body"])
    if "text" not in data or "checked" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # update the todo in the database
    result = table.update_item(
        Key={"id": event["pathParameters"]["id"]},
        ExpressionAttributeNames={
            "#todo_text": "text",
        },
        ExpressionAttributeValues={
            ":text": data["text"],
            ":checked": True,
            ":updatedAt": timestamp,
        },
        UpdateExpression="SET #todo_text = :text, "
                         "checked = :checked, "
                         "updatedAt = :updatedAt",
        ReturnValues="ALL_NEW",
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": deserialize_item(result["Attributes"]),
    }

    return response
