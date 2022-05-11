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

def send_to_s3(file, app):
    print('file>>>>>>>',file.filename)
    try:
        s3.upload_file(data, os.environ['BUCKET_NAME'], "testfile")
    except Exception as e:
        print("Something Happened: ", e)  
        return e
    return "{}{}".format(app.config["S3_LOCATION"], str(file.filename))
