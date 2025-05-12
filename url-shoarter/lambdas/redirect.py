import json
import os
import time

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    short_code = event["pathParameters"]["short_code"]
    response = table.get_item(Key={"short_code": short_code})

    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Not found"})}

    record = short_code["Item"]

    # Check if url has reached max redirections
    if record.get("attempts"):
        if record.get("attempts") <= 0:
            return {"statusCode": 400, "body": json.dumps({"error": "Max redirect attempts reached"})}
        else:
            table.update_item(
                Key={"id": event["pathParameters"]["id"]},
                ExpressionAttributeNames={
                    "#attempts": "attempts",
                },
                ExpressionAttributeValues={
                    ":attempts": record["attempts"] - 1
                },
                UpdateExpression="SET #attempts = :attempts",
                ReturnValues="ALL_NEW",
            )
    # Deadline when link must be inactive
    if record.get("end_date") and record.get("end_date") >= int(time.time() * 1000):
        return {"statusCode": 400, "body": json.dumps({"error": "Link expired"})}

    return {
        "statusCode": 302,
        "headers": {"Location": response["Item"]["original_url"]}
    }
