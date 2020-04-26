'''
lambda/ZygardeS3Output

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
import logging
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

SUBJECT = os.environ['SUBJECT']
EMAIL_SENDER = os.environ['EMAIL_SENDER']
CHARSET = os.environ['CHARSET']

logging.basicConfig(level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s')

def get_s3_object_stream(bucket, key, charset):
    try:
        streaming_body = s3_client.get_object(Bucket=bucket, Key=key,
                ResponseContentEncoding=charset)['Body']
        title = next(streaming_body.iter_lines()).decode(charset)
        streaming_body.close()

        streaming_body = s3_client.get_object(Bucket=bucket, Key=key,
                ResponseContentEncoding=charset)['Body']
        body = streaming_body.read().decode(charset)
        streaming_body.close()
        
        logging.info('Training result report retrieved!')
    except ClientError as ce:
        logging.error('get_s3_object_stream: s3 client error while getting S3 file\'s stream')
        logging.error(ce['Error']['Message'])
        return (None, None)

    return title, body

def send_email(recipient, body_text, subject, charset):
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': charset,
                        'Data': body_text
                    }
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject
                }
            },
            Source=EMAIL_SENDER
        )
        logging.info(f'Email sent! MessageID: {response["MessageId"]}')
    except ClientError as ce:
        logging.error('send_email: ses client error while sending email')
        logging.error(ce['Error']['Message'])

def build_message_from_event_record(record):
    bucket = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key'].replace('%40', '@')
    split_path_index = str.index(object_key, '/')
    email_address = object_key[: split_path_index]
    job = object_key[split_path_index+1 : str.rindex(object_key, '.')]

    _, message_body = get_s3_object_stream(bucket, object_key, CHARSET.lower())

    return {
        'uuid': job,
        'recipient': email_address,
        'body': message_body
    }

def lambda_handler(event, context=None):
    for record in event['Records']:
        logging.info(f'Received message event: {record["s3"]["bucket"]["name"]}/{record["s3"]["object"]["key"]}')
        
        msg = build_message_from_event_record(record)

        subject = f'{SUBJECT} - {msg["uuid"]}'
        send_email(msg['recipient'], msg['body'], subject, CHARSET.upper())

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
