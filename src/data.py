import os
import boto3
import pandas as pd

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT_URL", "https://storage.yandexcloud.net"),
        region_name="ru-central1",
    )

def read_s3_csv(bucket, key):
    response = get_s3_client().get_object(Bucket=bucket, Key=key)
    return pd.read_csv(response["Body"])