import json
import os
import time
from json import JSONDecodeError
from uuid import uuid4

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def generate_short_code():
    return str(uuid4())[:8]


def lambda_handler(event, context):
    # Handle empty body
    if not event["body"]:
        return {
            "statusCode": 400,
            "body": json.dumps({"status": False, "message": "No body provided"})
        }

    # Handle not valid body
    try:
        body = json.loads(event["body"])
    except JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"status": False, "message": "Wrong body provided"})
        }

    # Get url from
    original_url = body.get("url")
    if not original_url:
        return {"statusCode": 400, "body": json.dumps({"error": "URL is required"})}

    short_code = generate_short_code()

    basic_record = {
        "short_code": short_code,
        "original_url": original_url,
        "updated_at": int(time.time() * 1000)
    }

    # Get some additional settings

    # How much times link can be used
    attempts = body.get("attempts")
    if attempts:
        basic_record["attempts"] = attempts

    # Deadline when link must be inactive
    end_date = body.get("end_date")
    if end_date:
        basic_record["end_date"] = end_date

    table.put_item(
        Item=basic_record
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
                               "shortened_url": f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}/{short_code}"})
    }
