import boto3
import os
from dotenv import load_dotenv
load_dotenv()


s3 = boto3.client( 
  "s3",
  "us-west-1",
  aws_access_key_id=os.environ['KEY_ID'],
  aws_secret_access_key=os.environ['ACCESS_KEY'],
)

s3.upload_file('sample.avif',os.environ['BUCKET_NAME'], 'sample.avif')
print(s3)
