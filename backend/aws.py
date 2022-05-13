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


def send_to_s3(file, location):
    """ Accepts file and app and uploads to aws s3. """

    try:
        s3.put_object(
            Body=file,
            Bucket=os.environ['BUCKET_NAME'],
            Key=file.filename,
            ContentType= "image/jpeg"
            )
        # s3.upload_file(
        #   file.filename, os.environ['BUCKET_NAME'], file.filename,
        #                ExtraArgs={
        #     "ContentType": "image/jpeg"
        # })
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(location, str(file.filename))
