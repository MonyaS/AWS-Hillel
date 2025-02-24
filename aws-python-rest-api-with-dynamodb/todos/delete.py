import json
import os

import boto3
from boto3.dynamodb.conditions import Key

from utils.auth_decorator import token_required

dynamodb = boto3.resource("dynamodb")


@token_required
def delete(event, context, username):
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    # delete the todo from the database
    result = table.scan(
        FilterExpression=Key('id').eq(event["pathParameters"]["id"]) & Key('user').eq(username)
    )
    if result["Items"]:
        table.delete_item(Key={"id": event["pathParameters"]["id"]})
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Todo not found.'})
        }
    # create a response
    response = {"statusCode": 200}

    return response
