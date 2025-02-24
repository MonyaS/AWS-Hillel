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

    record = response["Item"]

    # Check if url has reached max redirections
    if "attempts" in record.keys():
        if record.get("attempts") <= 0:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Max redirect attempts reached"}),
            }
        else:
            table.update_item(
                Key={"short_code": event["pathParameters"]["short_code"]},
                ExpressionAttributeNames={
                    "#attempts": "attempts",
                },
                ExpressionAttributeValues={
                    ":attempts": record.get("attempts") - 1,
                },
                UpdateExpression="SET #attempts = :attempts",
                ReturnValues="ALL_NEW",
            )

    # Deadline when link must be inactive
    if record.get("end_date") and record.get("end_date") <= int(time.time() * 1000):
        return {"statusCode": 400, "body": json.dumps({"error": "Link expired"})}

    # update the todo in the database
    table.update_item(
        Key={"short_code": event["pathParameters"]["short_code"]},
        ExpressionAttributeNames={
            "#last_use": "last_use",
        },
        ExpressionAttributeValues={
            ":last_use": int(time.time() * 1000)
        },
        UpdateExpression="SET #last_use = :last_use",
        ReturnValues="ALL_NEW",
    )

    return {
        "statusCode": 302,
        "headers": {"Location": response["Item"]["original_url"]},
    }
