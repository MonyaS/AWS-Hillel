import os

import boto3

from utils.auth_decorator import token_required

dynamodb = boto3.resource("dynamodb")


@token_required
def delete(event, context, username):
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # delete the todo from the database
    table.delete_item(Key={"id": event["pathParameters"]["id"]})

    # create a response
    response = {"statusCode": 200}

    return response
