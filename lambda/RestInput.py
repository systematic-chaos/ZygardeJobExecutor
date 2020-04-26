'''
lambda/RestInput

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
import boto3
from botocore.exceptions import ClientError

sqs_client = boto3.client('sqs')

OUTPUT_QUEUE = 'ZygardeQueue'
OUTPUT_QUEUE_URL = sqs_client.get_queue_url(QueueName=OUTPUT_QUEUE)['QueueUrl']

def send_sqs_message(msg):
    try:
        msg = sqs_client.send_message(QueueUrl=OUTPUT_QUEUE_URL, MessageBody=msg)
    except ClientError as ce:
        print('send_sqs_message: sqs client error while sending message')
        print(ce['Error']['Message'])
        return None
    print(f'Sent SQS message ID: {msg["MessageId"]}')
    return msg

def lambda_handler(event, context=None):
    print(f'Received request body: {event["body"]}')
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

with open('request-body-full.json', 'r') as input_file:
    event = {'body': input_file.read()}
lambda_handler(event, {'outputQueue': OUTPUT_QUEUE})
