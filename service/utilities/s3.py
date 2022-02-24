import os
import boto3
import botocore
import datetime

s3 = None



key_id = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
bucket = os.environ.get('AWS_S3_BUCKET')
prefix = os.environ.get('AWS_S3_PREFIX', 'ai-sensor')

if key_id and secret_key and bucket:
    session = boto3.session.Session(aws_access_key_id=key_id,
                                    aws_secret_access_key=secret_key)
    s3 = session.resource(
        's3',
        config=botocore.client.Config(signature_version='s3v4')
    )
    print(f'S3 information found.  Will save request body to bucket {bucket}')
else:
    print(f'S3 information not found.  Will NOT save request body')



def save_json(data):
    if s3 is None:
        return

    obj_key = f'{datetime.datetime.now().isoformat()}.json'
    s3.Object(bucket, os.path.join(prefix, obj_key)).put(Body=data)


