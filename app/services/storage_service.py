
import os
import boto3
import mimetypes
from app.config import (
    SUPABASE_S3_ENDPOINT,
    SUPABASE_ACCESS_KEY,
    SUPABASE_SECRET_KEY,
    SUPABASE_BUCKET,
)



print("ENDPOINT:", os.getenv("SUPABASE_S3_ENDPOINT"))
print("ACCESS:", bool(os.getenv("SUPABASE_ACCESS_KEY")))
print("SECRET:", bool(os.getenv("SUPABASE_SECRET_KEY")))

class StorageService:

    @staticmethod
    def get_client():
        return boto3.client(
            "s3",
            endpoint_url=SUPABASE_S3_ENDPOINT,
            aws_access_key_id=SUPABASE_ACCESS_KEY,
            aws_secret_access_key=SUPABASE_SECRET_KEY,
            region_name="ap-south-1",
        )

    
    @staticmethod
    def create_upload_url(path: str, mime_type: str):
        s3 = StorageService.get_client()

        return s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": SUPABASE_BUCKET,
                "Key": path,
                "ContentType": mime_type,
            },
            ExpiresIn=3600,
        )

    
    @staticmethod
    def create_download_url(path: str):
        s3 = StorageService.get_client()

        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": SUPABASE_BUCKET,
                "Key": path,
            },
            ExpiresIn=3600,
        )

    
    @staticmethod
    def file_exists(path: str):
        s3 = StorageService.get_client()

        try:
            s3.head_object(Bucket=SUPABASE_BUCKET, Key=path)
            return True
        except s3.exceptions.ClientError:
            return False

    
    @staticmethod
    def download_file(key: str, local_path: str):
        s3 = StorageService.get_client()
        s3.download_file(SUPABASE_BUCKET, key, local_path)



    @staticmethod
    def upload_file(local_path: str, storage_key: str):
        s3 = StorageService.get_client()
        bucket = os.getenv("SUPABASE_BUCKET")

    
        content_type, _ = mimetypes.guess_type(storage_key)

        if not content_type:
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        s3.upload_file(
            local_path,
            bucket,
            storage_key,
            ExtraArgs={
            "ContentType": content_type
        }
    )


