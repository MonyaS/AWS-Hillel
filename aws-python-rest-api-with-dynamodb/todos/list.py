import json
import logging
import os

import boto3

from todos import decimalencoder
dynamodb = boto3.resource("dynamodb")


def list_lambda(event, context):
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # fetch all todos from the database
    result = table.scan()

    logging.info(result)
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder),
    }

    return response
