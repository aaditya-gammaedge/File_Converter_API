import boto3
from botocore.client import Config
from botocore.exceptions import ClientError




from app.config import (
    SUPABASE_S3_ENDPOINT,
    SUPABASE_ACCESS_KEY,
    SUPABASE_SECRET_KEY,
    SUPABASE_BUCKET,
)




s3_client = boto3.client(
    "s3",
    endpoint_url=SUPABASE_S3_ENDPOINT,
    aws_access_key_id=SUPABASE_ACCESS_KEY,
    aws_secret_access_key=SUPABASE_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)


def delete_from_s3(key: str):
    try:
        s3_client.delete_object(
            Bucket=SUPABASE_BUCKET,
            Key=key,
        )
        print(f"Deleted from Supabase bucket: {key}")

    except ClientError as e:
        print(f"S3 deletion failed for {key}: {e}")
        raise e


