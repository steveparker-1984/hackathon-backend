import json
import os
import uuid
import boto3
from decimal import Decimal


def lambda_handler(event, context):

    print(json.dumps(event))

    if event['httpMethod'] == 'POST':
        print('Saving new order...')
        try:
            order = json.loads(event['body'])
        except:
            return respond({'error': 'Invalid request format.'}, True)
        try:
            result = process_new_order(order)
        except:
            return respond({'error': 'Unable to process order.'}, True)
    else:
        result = {}

    return respond(result)


def process_new_order(order):
    # if POST return generated order id
    order['orderId'] = str(uuid.uuid4())

    if 'userId' not in order:
        return respond({'error': 'Order is missing userId.'}, True)
    
    save_order_to_db(order)

    result = {
        'status': 'ok',
        'orderId': order['orderId']
    }

    return result


def save_order_to_db(order):

    replace_floats(order)
    print(order)
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_DEPLOY_REGION'])
    table = dynamodb.Table(os.environ['ORDER_TABLE'])
    response = table.put_item(Item=order)
    print(response)


def replace_floats(order):
    for item in order['items']:
        item['variant_price'] = Decimal(str(item['variant_price']))

        for k, v in item['additions'].items():
            item['additions'][k] = Decimal(str(v))


def respond(body, error=False):
    response = {
        "statusCode": 400 if error else 200,
        "body": json.dumps(body),
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            "Content-Type": "application/json"
        }
    }
    return response


# if __name__ == "__main__":
#     os.environ['ORDER_TABLE'] = 'coffee-orders'
#     os.environ['AWS_REGION'] = 'eu-west-2'

#     with open('example_order.json') as f:
#         data = json.load(f)

#     response = lambda_handler(data, None)
#     print(response)
