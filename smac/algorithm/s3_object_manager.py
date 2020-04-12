'''
algorithm/s3_object_manager
Manager for objects storage in Amazon Web Service Simple Storage Service (AWS S3)

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import boto3
from botocore.exceptions import ClientError
import os.path
import sys

s3_client = boto3.client('s3')

def upload_file(file_name, bucket, object_name):
    if not object_name:
        object_name = os.path.basename(file_name)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(object_name)
    except ClientError as ce:
        print(ce['Error']['Message'], file=sys.stderr)
        return False
    return True

def copy_s3_file(src_object, dest_object):
    try:
        s3_client.copy_object(CopySource=src_object,
            Bucket=dest_object["Bucket"], Key=dest_object["Key"])
        print(f'Copied {src_object["Key"]} file object from bucket \
            {src_object["Bucket"]} to {dest_object["Key"]} in bucket {dest_object["Bucket"]}')
    except ClientError as ce:
        print('copy_s3_file: s3 client error while copying object across buckets', file=sys.stderr)
        print(ce['Error']['Message'], file=sys.stderr)

def delete_s3_file(s3_object):
    try:
        s3_client.delete_object(Bucket=s3_object["Bucket"], Key=s3_object["Key"])
        print(f'Deleted {s3_object["Key"]} file object from bucket {s3_object["Bucket"]}')
    except ClientError as ce:
        print('delete_s3_file: s3 client error while deleting object', file=sys.stdout)
        print(ce['Error']['Message'], file=sys.stdout)

def create_presigned_url(s3_object, expiration=9000):
    return s3_client.generate_presigned_url('get_object',
                                            Params=s3_object,
                                            ExpiresIn=expiration)
