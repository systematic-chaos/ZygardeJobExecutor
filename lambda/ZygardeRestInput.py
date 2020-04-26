'''
lambda/ZygardeRestInput

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
import logging
import boto3
from botocore.exceptions import ClientError

sqs_client = boto3.client('sqs')

OUTPUT_QUEUE_URL = sqs_client.get_queue_url(QueueName=os.environ['OUTPUT_QUEUE'])['QueueUrl']

logging.basicConfig(level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s')

def send_sqs_message(msg):
    try:
        msg = sqs_client.send_message(QueueUrl=OUTPUT_QUEUE_URL, MessageBody=msg)
    except ClientError as ce:
        logging.error('send_sqs_message: sqs client error while sending message')
        logging.error(ce['Error']['Message'])
        return None
    logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
    return msg

def lambda_handler(event, context):
    logging.info(f'Received request body: {event["body"]}')
    msg_response = send_sqs_message(event['body'])
    if msg_response:
        return {
            'statusCode': 200,
            'body': json.dumps(msg_response)
        }
    else:
        return {
            'statusCode': 400
        }
