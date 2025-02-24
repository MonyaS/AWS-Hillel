import json
import os

import boto3

from utils import DecimalEncoder

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    short_code = event["pathParameters"]["short_code"]
    response = table.get_item(Key={"short_code": short_code})

    # Check if item exist
    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Not found"})}

    # Get item
    record = response["Item"]

    # Return item info
    return {"statusCode": 200, "body": json.dumps(record, cls=DecimalEncoder)}
