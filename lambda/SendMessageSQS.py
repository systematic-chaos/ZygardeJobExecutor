'''
lambda/SendMessageSQS

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import os.path
import sys
import boto3
from botocore.exceptions import ClientError

QUEUE_NAME = 'ZygardeQueue'

sqs_client = boto3.client('sqs')

def send_sqs_message(queue, msg):
    try:
        msg = sqs_client.send_message(QueueUrl=queue, MessageBody=msg)
    except ClientError as ce:
        print('send_sqs_message: sqs client error while sending message')
        print(ce['Error']['Message'])
        return None
    print(f'Sent SQS message ID: {msg["MessageId"]}')
    return msg

def main():
    queue = sys.argv[1] if len(sys.argv) > 1 else QUEUE_NAME
    if len(sys.argv) > 2:
        json_files = sys.argv[2:]
    else:
        json_files = ['request-body.json', 'request-body-full.json']

    queue = sqs_client.get_queue_url(QueueName=queue)
    print(queue)

    for json_file in json_files:
        with open(json_file, 'r') as jf:
            send_sqs_message(queue['QueueUrl'], jf.read())
        print(json_file)

if __name__ == "__main__":
    main()
