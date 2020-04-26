import boto3
import json
import os
import uuid
from botocore.exceptions import ClientError
from urllib.parse import unquote_plus

s3_client  = boto3.client('s3')
sqs_client = boto3.client('sqs')

OUTPUT_QUEUE = 'ZygardeQueue'
OUTPUT_QUEUE_URL = sqs_client.get_queue_url(QueueName=OUTPUT_QUEUE)['QueueUrl']

def get_s3_file(record):
    bucket = record['bucket']['name']
    key = unquote_plus(record['object']['key'])
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), key.replace('/', ''))
    try:
        s3_client.download_file(bucket, key, download_path)
    except ClientError as ce:
        print('get_s3_file: s3 client error while downloading file')
        print(ce['Error']['Message'])
        return ''
    print(f'Downloaded {bucket}/{key} file to {download_path}')
    return download_path

def send_sqs_message(msg_path):
    with open(msg_path, 'r') as msg_file:
        try:
            msg = sqs_client.send_message(QueueUrl=OUTPUT_QUEUE_URL, MessageBody=msg_file.read())
        except ClientError as e:
            print('send_sqs_message: sqs client error while sending message')
            print(e)
            return None
        print(f'Sent SQS message ID: {msg["MessageId"]}')
        return msg

def lambda_handler(event, context=None):
    for record in event['Records']:
        print(f'Received event record: {json.dumps(record)}')
        file_path = get_s3_file(record['s3'])
        if not file_path:
            return {
                'statusCode': 400
            }
        send_sqs_message(file_path)
        os.remove(file_path)
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

with open('S3ObjectCreateEvent.json', 'r') as input_file:
    event = json.load(input_file)
lambda_handler(event, {'outputQueue': OUTPUT_QUEUE})
