from __future__ import print_function
import boto3
import logging
import os
import uuid
import json

from botocore.config import Config
from botocore.exceptions import ClientError

bucket_name = os.environ['IMAGE_UPLOAD_BUCKET']
runtime_region = os.environ['AWS_REGION']

my_config = Config(
    signature_version='s3v4',
    s3={'addressing_style': 'virtual'}
)

# --------------- Main handler ------------------
def lambda_handler(event, context):
    s3_client = boto3.client(
        's3', region_name=runtime_region, config=my_config)
    try:
        file_name = uuid.uuid4().hex + '.jpg'
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': file_name,
                                                            'ContentType': 'image/jpeg'},
                                                    ExpiresIn=300)
    except ClientError as e:
        logging.error(e)
        return None

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "uploadURL": response,
            "Key": file_name
        })
    }
