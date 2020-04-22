'''
lambda/S3Output

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import json
import boto3
from botocore.exceptions import ClientError

s3_client  = boto3.client('s3')
ses_client = boto3.client('ses')

SUBJECT = 'Zygarde'
EMAIL_SENDER = 'thanatos.dreamslayer@gmail.com'
CHARSET = 'UTF-8'

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
        
        print('Training result report retrieved!')
    except ClientError as ce:
        print('get_s3_object_stream: s3 client error while getting S3 file\'s stream')
        print.error(ce['Error']['Message'])
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
        print(f'Email sent! Message ID: {response["MessageId"]}')
    except ClientError as ce:
        print('send_email: ses client error while sending email')
        print(ce['Error']['Message'])

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
        print(f'Received message event: {record["s3"]["bucket"]["name"]}/{record["s3"]["object"]["key"]}')
        
        msg = build_message_from_event_record(record)
        
        subject = f'{SUBJECT} - {msg["uuid"]}'
        send_email(msg['recipient'], msg['body'], subject, CHARSET.upper())

with open('S3ObjectCreateEvent.json', 'r') as input_file:
    event = json.load(input_file)
lambda_handler(event)
