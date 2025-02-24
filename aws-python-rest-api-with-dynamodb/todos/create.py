import json
import logging
import os
import time
import uuid

import boto3

from utils.auth_decorator import token_required
from utils.serializer import deserialize_item

dynamodb = boto3.resource("dynamodb")


@token_required
def create(event, context, username):
    data = json.loads(event["body"])
    if "text" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    item = {
        "id": str(uuid.uuid1()),
        "text": data["text"],
        "checked": False,
        "createdAt": timestamp,
        "updatedAt": timestamp,
        "user": username,
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {"statusCode": 200, "body": deserialize_item(item)}

    return response
