'''
lambda/ZygardeS3Input

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import json
import os
import uuid
import logging
import boto3
from botocore.exceptions import ClientError
from urllib.parse import unquote_plus

s3_client  = boto3.client('s3')
sqs_client = boto3.client('sqs')

OUTPUT_QUEUE_URL = sqs_client.get_queue_url(QueueName=os.environ['OUTPUT_QUEUE'])['QueueUrl']

logging.basicConfig(level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s')

def get_s3_file(record):
    bucket = record['bucket']['name']
    key = unquote_plus(record['object']['key'])
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), key.replace('/', ''))
    try:
        s3_client.download_file(bucket, key, download_path)
    except ClientError as ce:
        logging.error('get_s3_file: s3 client error while downloading file')
        logging.error(ce['Error']['Message'])
        return ''
    logging.info(f'Downloaded {bucket}/{key} file to {download_path}')
    return download_path

def send_sqs_message(msg_path):
    with open(msg_path, 'r') as f:
        try:
            msg = sqs_client.send_message(QueueUrl=OUTPUT_QUEUE_URL, MessageBody=f.read())
        except ClientError as e:
            logging.error('send_sqs_message: sqs client error while sending message')
            logging.error(e)
            return None
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
    return msg
    
def lambda_handler(event, context):
    for record in event['Records']:
        logging.info(f'Received event record: {json.dumps(record)}')
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
