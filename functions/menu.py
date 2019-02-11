import json
import boto3
import botocore

BUCKET_NAME = 'covfefe-assets'
KEY = 'static-json/menu.json'

def lambda_handler(event, context):

    boto3.resource('s3').Bucket(BUCKET_NAME).download_file(KEY, '/tmp/menu.json')

    with open('/tmp/menu.json') as f:
        data = json.load(f)

    return respond(data)


def respond(body):
    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            "Content-Type": "application/json"
        }
    }
    return response
