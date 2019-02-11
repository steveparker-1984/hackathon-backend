import boto3
import json
from decimal import Decimal

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('coffee-orders')

    response = table.scan()

    items = response['Items']

    print(items)

    return respond(items)

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

def respond(body):
    response = {
        "statusCode": 200,
        "body": json.dumps(body, cls=CustomJsonEncoder),
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            "Content-Type": "application/json"
        }
    }
    return response


if __name__ == "__main__":
    lambda_handler(None, None)
